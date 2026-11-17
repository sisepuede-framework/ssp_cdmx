# SSP_CDMX

This repository contains notebooks and supporting files used to run the
**SISEPUEDE** model on Mexico City's (CDMX) mitigation scenarios. All modeling
resources reside in the `ssp_modeling` folder described below.


## Instructions: Setting Up the SISEPUEDE Environment

### 1. **Go to the `environment.yml` file**

Obtain the provided `environment.yml` file for SISEPUEDE.

### 2. **Set a Custom Environment Name**

Open the `environment.yml` file in your preferred text editor (such as VS Code, Atom, nano, or even Notepad).
At the very top, you'll see a line like:

```yaml
name: ssp_cdmx
```

**Change `ssp_cdmx` to your preferred environment name if you like.**

### 3. **Create the Environment from the `.yml` File**

In your terminal, navigate to the directory containing your `environment.yml` file, then run:

```bash
conda env create -f environment.yml
```

This will create a new Conda environment with the name you set in the file.

### 4. **Activate the Environment**

After installation, activate your new environment with:

```bash
conda activate <your_env_name>
```

*(Replace `<your_env_name>` with the name you specified in the `.yml` file, e.g., `ssp_cdmx`)*


### 5. **Done!**

Your environment is now ready to use, with all dependencies (including those installed via pip) preconfigured.


#### **Tips:**

* If you update the `environment.yml` file later, you can update your environment with:

  ```bash
  conda env update -f environment.yml --prune
  ```
* You can list all your environments with:

  ```bash
  conda env list
  ```
* The energy model (NemoMod) runs on Julia through `juliacall`. The first run
  precompiles Julia (~2 min) and may print a method-overwrite `ERROR` line; it does
  not stop the run.

## Project Structure

The most relevant files are inside the `ssp_modeling` directory:

- `config_files/` – YAML configuration file used by the notebook.
- `input_data/` – SISEPUEDE input CSV for CDMX (`sisepuede_adj_inputs_CDMX.csv`).
- `notebooks/` – `cdmx_manager.ipynb`, the notebook that manages the modeling runs, plus `shared_scripts/` for postprocessing and cost-benefits.
- `ssp_run_output/` – Output folders created after executing a scenario.
- `scenario_mapping/` – Spreadsheets with the mapping between SSP transformations and CDMX measures (PACCM). This is where the scenarios and transformation intensities are defined.
- `transformations/` – CSVs and YAML files describing the transformations applied by the model.
- `cost-benefits/` – Configuration for the cost-benefit analysis.
- `output_postprocessing/` – Scripts and crosswalks used to process model results.
- `tableau/` – Tableau dashboard (`CDMX_CaseStudy.twbx`).

## Steps to run the model and load data to Tableau for analysis

All files and folders referenced here are inside the `ssp_modeling` directory.

1. **Run the model in the notebook**

   * Edit the configuration file in `config_files/config.yaml`. Keep `country_name: "mexico"`: it is the only region label SISEPUEDE recognizes; outputs are relabeled `cdmx` during postprocessing.
   * Set up the transformations spreadsheet for custom Strategies and save it in `scenario_mapping/` (default: `ssp_cdmx_transformation_strategy.xlsx`).
   * Open `notebooks/cdmx_manager.ipynb` and run the cells to execute the model. Set `strategies_to_run` to the strategy ids you want (default `[0, 6004]`: BASE and PACCM).

2. **Post-process results**

   * The last cells of the notebook write `decomposed_ssp_output.csv` in the run folder and build the Tableau tables (emissions, drivers, levers) in `tableau/data/`.
   * The cost-benefit cell compares each strategy against BASE and writes `tableau/data/cb_data.csv`.

3. **Load data into Tableau**

   * Open `tableau/CDMX_CaseStudy.twbx`.
   * Point it to the files in `tableau/data/` (`emissions_cdmx_2022.csv`, `drivers_cdmx.csv`, `cb_data.csv`).
