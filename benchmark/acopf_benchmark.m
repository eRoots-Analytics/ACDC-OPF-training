% acopf_benchmark.m
% Batch AC-OPF over data/pglib_opf/*.m with MATPOWER, saving CSV
clear; clc;

%% --- MATPOWER path (uncomment & set if needed) ---
% MATPOWER_ROOT = '/absolute/path/to/matpower';
% run(fullfile(MATPOWER_ROOT, 'startup.m'));

%% --- Config ---
folder  = fullfile('data', 'pglib_opf');
out_csv = 'ACOPF_benchmark_matpower.csv';

% Solver/options
mpopt = mpoption('verbose', 0, 'out.all', 0, 'opf.ac.solver', 'MIPS');
% (optionally set tolerances)
% mpopt = mpoption(mpopt, 'mips.feastol',1e-6,'mips.gradtol',1e-6,'mips.comptol',1e-6,'opf.violation',1e-6);

files = dir(fullfile(folder, '*.m'));
if isempty(files)
    warning('No .m case files found under: %s', folder);
end

rows = struct([]);   % struct array, avoids length mismatches
ridx = 0;

fprintf('Found %d case files\n', numel(files));
fprintf('Running AC-OPF...\n\n');

for k = 1:numel(files)
    name  = files(k).name;
    fpath = string(fullfile(files(k).folder, name));

    fprintf('%s\nCase: %s\n', repmat('-',1,80), name);

    % Prepare a default row so even failures produce a complete row
    R = struct( ...
        'name',            string(name), ...
        'path',            fpath, ...
        'n_buses',         NaN, ...
        'n_branches',      NaN, ...
        'n_generators',    NaN, ...
        'Converged',       false, ...
        'time_s',          NaN, ...
        'objective',       NaN, ...
        'Error',           "", ...
        'final_feascond',  NaN, ...
        'final_gradcond',  NaN, ...
        'final_compcond',  NaN, ...
        'final_costcond',  NaN, ...
        'mips_feastol',    mpopt.mips.feastol, ...
        'mips_gradtol',    mpopt.mips.gradtol, ...
        'mips_comptol',    mpopt.mips.comptol, ...
        'opf_violation',   mpopt.opf.violation, ...
        'solver',          string(mpopt.opf.ac.solver) ...
    );

    try
        % Load and basic sizes
        mpc = loadcase(char(fpath));
        R.n_buses      = size(mpc.bus,    1);
        R.n_branches   = size(mpc.branch, 1);
        R.n_generators = size(mpc.gen,    1);

        % Solve
        t_start  = tic;
        results  = runopf(mpc, mpopt);
        R.time_s = toc(t_start);

        % Status, objective, message
        R.Converged = isfield(results, 'success') && results.success == 1;
        if isfield(results, 'f'), R.objective = results.f; end
        if isfield(results, 'raw') && isfield(results.raw, 'output') && isfield(results.raw.output, 'message')
            R.Error = string(results.raw.output.message);
        end

        % Final KKT residuals from MIPS (if available)
        if isfield(results, 'raw') && isfield(results.raw, 'output') && isfield(results.raw.output, 'hist')
            h = results.raw.output.hist;
            if ~isempty(h)
                R.final_feascond = h(end).feascond;
                R.final_gradcond = h(end).gradcond;
                R.final_compcond = h(end).compcond;
                R.final_costcond = h(end).costcond;
            end
        end

        fprintf('Converged : %s\n', string(R.Converged));
        fprintf('Time (s)  : %.6f\n', R.time_s);
        if ~isnan(R.final_feascond)
            fprintf('Final KKT : feas=%.3e, grad=%.3e, comp=%.3e, cost=%.3e\n', ...
                R.final_feascond, R.final_gradcond, R.final_compcond, R.final_costcond);
        end
        if ~R.Converged && strlength(R.Error) > 0
            fprintf('Message   : %s\n', R.Error);
        end

    catch ME
        % Fill error message, sizes may already be set if load succeeded
        R.Error = string(ME.message);
        fprintf('ERROR: %s\n', ME.message);
    end

    ridx = ridx + 1;
    rows(ridx) = R;  %#ok<SAGROW> % append one complete row
    fprintf('%s\n', repmat('-',1,80));
end

% Convert to table (all rows have identical fields)
T = struct2table(rows);

% (Optional) quick sanity check
% disp([height(T), width(T)]);
% disp(T(:, {'name','n_buses','n_branches','n_generators','Converged','time_s'}));

% Save CSV
writetable(T, out_csv);
fprintf('\nSaved results to: %s\n', out_csv);
