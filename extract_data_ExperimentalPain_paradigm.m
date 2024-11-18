function extract_data_ExperimentalPain_paradigm

% extracts MRI data [durations, onsets ...] simultaneously with ratings from logfiles
% all onset files and rating files are written outside of the BIDS
% structure (i.e. in sourcedata) in order to be flexible with the structure
% and not mess up BIDS validation

% Isabel Ellerbrock, June 2021

base        = '/data/isabel/POADOS';
logDir      = [base filesep 'BIDS/sourcedata/logfiles'];
outDir      = [base filesep 'BIDS/sourcedata/matfiles'];
run         = {'ExpPain1';'ExpPain2'};
sess        = {'pre'};  % 'post'

% exceptions are handled below
% 1010 ExpPain2 missing
% 1020 ExpPain2
% 1022 ExpPain2 (has been edited and implemented for final file "all_scores")

% specify subjects and group association
subjects    = {[1008 1010 1011 2003 1013 1015 1017 1019 1020 1021 1022]
               [4102 4103 4104 4105 4106 4108 4109 4110 4111 4113 4114 4115 4116 4117 4118 4119 4121]};
group  = [];  % currently there are two groups: (DDD and HCDDD) but can be extendend if needed
for ng = 1:length(subjects)
    group = [group ones(1,length(subjects{ng}))*ng];  % subs will be assigned to a group
end
maxsub = max([length(subjects{1}) length(subjects{2})]);  % max number of subs in whatever group is the max for all groups (add if neccessary)
reps = 1:20;  % number of repetitions for each stim intensitiy (summed over two runs)

% four-dimensional final file: 2 x 20 x Y x 2
% 2 (conditions: pain/sensory) x 20 (repetitions: 10 pain + 10 sens) x maximum number of subjects in a group x 2 (number of groups)
all_scores = NaN(2,length(reps),maxsub,max(group));

% loop over groups (g)
for g = 1:numel(subjects)   % number of elements in subjects = groups
    inx = 0;    % subject counter within each group

    % loop over subjects in each group (s)
    for s = subjects{g} 
        inx = inx+1;
        name = strcat('sub-', sprintf('%02.3d', s));

        fprintf('\n'); disp(['---> extract data: ' name])

        % create empty variable for each score type (pain and sensory) and combined scores (ExpPain)
        ExpPain_scores = []; pain_scores = []; sens_scores = [];
        c = 0; d = 0;

        % loop over runs (r)
        for r = 1:length(run)

            % check if ExpPain (run1 and run2) paradigm were run and therefore a logfile exists. If yes, continue:
            if isfile(fullfile(logDir, run{r}, [num2str(s) '_' sess{1} '-POADOS_' run{r} '.log']))

                % read in logfile
                fid = fopen(fullfile(logDir, run{r}, [num2str(s) '_' sess{1} '-POADOS_' run{r} '.log']));
                E = textscan(fid, '%*s %q %q %q %f %*s %*s %*s %*[^\n]', 'headerlines', 5, 'delimiter', '\t');
                fclose(fid);

                % find positions for each relevant information in large logfile matrix E
                trial = E{1};
                event = E{2};   % automatic event info 
                code  = E{3};   % individually coded event info
                time  = E{4};   % all temporal information

                % extract subject's rating here
                score_column = char(code(strmatch('SCORE:',code))); % extract columns where rating was done by searching for 'score'
                scores = str2num(score_column(:,7:end));            % extract only the number, not the word 'score'

                % exception in sub-1022, data was collected faulty due to APA misfunction
                % scores are replaced by NaNs in trials where pressure intensity was
                % supposed to be "high" but was delivered as "low" in ExpPain 2
                if s == 1022 && r == 2     
                    scores([9 13 14 16:18], :) = NaN;
                end

                % define individual order of sensory and pain ratings and split
                % into stim intensity
                ini = 1; k = NaN(20,2);
                for i = 1:length(code)
                    if strcmp('SENSORY',code{i})
                        k(ini,2) = 0; k(ini,1) = ini; ini = ini+1;
                    elseif strcmp('PAIN',code{i})
                        k(ini,2) = 1; k(ini,1) = ini; ini = ini+1;
                    end
                end

                % use assembled individual mask to identify pain and sensory stim
                MSK_pain = (k(:,2) == 1);
                MSK_sens = (k(:,2) == 0);
                p_scores = scores(MSK_pain);
                s_scores = scores(MSK_sens);

                % exception in sub-1020 in ExpPain2
                if s == 1020 && r == 2
                    p_scores = NaN(10,1);
                    s_scores = scores;
                end

                % print ratings to the terminal
                disp(['--> pain scores (' run{r} '): ' num2str(p_scores')]);
                disp(['--> sensory scores (' run{r} '): ' num2str(s_scores')]);
                %pause(4);

                % insert scores into variable ExpPain_scores
                eval(['ExpPain_scores{' num2str(d+1) '} = [p_scores];' ]) 
                eval(['ExpPain_scores{' num2str(d+2) '} = [s_scores];' ])

                pain_scores = [pain_scores; p_scores];  % include p_ratings from both runs into one variable
                sens_scores = [sens_scores; s_scores];  % include s_ratings from both runs into one variable


                %%% MRI data
                % find beginning of experiment
                startTime = time(strmatch('0',strvcat(trial)))/10000; % convert milisec to sec by division of 10000. If not, it's in scan time
                %startTime = time(strmatch('0',strvcat(trial)))/10000/2.205; % convert milisec to sec by division of 10000 by division of TR in s, i.e. scan time
                startTime = startTime(1); % in case there are two 0 in the beginning of the logfile, take the first as start time 

                % The positions of each event in the big logfile matrix E
                painPos = strcmp('PAIN',code);     % position of pain stim trigger, i.e. will be onset of pain stim
                sensPos = strcmp('SENSORY',code);  % position of sensory stim trigger, i.e. will be onset of sensory stim
                vasPos  = strcmp('VAS',code);      % position of start of 7s rating period, i.e. will be onset of rating time
                % bpspos = strmatch('Response',event);  % could also be determined by participants response, e.g. individual button presses
                % pulsePos = strcmp('Pulse',event);  % currently not in use

                % give names
                names{c+1} = 'pain';
                names{c+2} = 'sensory';
                names{c+3} = 'vas';    % 'bps', if button presses are used

                % find onsets
                onsets{c+1} = ((time(painPos)/10000) - startTime)'; % onsets of painful stim
                onsets{c+2} = ((time(sensPos)/10000) - startTime)'; % onsets of sensory stim
                onsets{c+3} = ((time(vasPos)/10000) - startTime)';  % onsets of vas

                % define durations
                durations{c+1} = repmat(5,1,10);    % duration of each pain stim, 5s (10 in total per run)
                durations{c+2} = repmat(5,1,10);    % duration of each sensory stim, 5s (10 in total per run)
                durations{c+3} = repmat(7,1,20);    % duration of rating time, 7s (20 rating times in total per run)

                % save onsets etc for fmri first level analysis, one for each run
                % mFile = fullfile(base, 'BIDS', name, ['ses-' sess{1}], 'func', [name '_ses-' sess{1} '_task-' run{r}(1:end-1) '_run-' run{r}(end) '_events.mat']);
                mFile = fullfile(outDir, [name '_ses-' sess{1} '_task-' run{r}(1:end-1) '_run-' run{r}(end) '_events.mat']);
                save(mFile, 'names', 'onsets', 'durations');

            else
                % if (this part of) ExpPain was not run, insert NaN
                pain_scores = [pain_scores; NaN(10,1)];
                sens_scores = [sens_scores; NaN(10,1)];
            end

            d=d+2;
        end

        %%% Rating data
        % stim intensity x stim number x max subject in one group x groups, e.g.: 2 x 20 x 16 x 2
        all_scores(1,:,inx,g) = pain_scores;
        all_scores(2,:,inx,g) = sens_scores;

        eval(['ExpPain_scores{' num2str(d+1) '} = name(1,:) ;' ])   % add the subject code in overall file

        % save individual rating data
        rFile = fullfile(outDir, [name '-ses-' sess{1} '-ExpPain_scores.mat']);
        save(rFile, 'pain_scores', 'sens_scores');

    end
end

% save all rating data for all participants in one file
asFile = fullfile(base, 'all_scores.mat');
save(asFile, 'all_scores')

end

