import aiofiles
import os
import subprocess
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from tempfile import TemporaryDirectory
from fastapi.responses import RedirectResponse

from .demands_analysis import RawDemandsAnalysis, AggregatedDemandsAnalysis

# load .env file
load_dotenv()

# create application
app = FastAPI()

# load the spacenet jar path from environment variable
spacenet_path = os.getenv("SPACENET_PATH")
if not os.path.exists(spacenet_path):
    raise (RuntimeError(f"SpaceNet JAR not found at: {spacenet_path}"))

# load the spacenet execution timeout from environment variable (default: 10 s)
spacenet_timeout = os.getenv("SPACENET_TIMEOUT", 10)


@app.get("/", include_in_schema=False)
async def docs_redirect():
    """"This function redirects the user to the '/docs' endpoint.
    Parameters:
        - None
    Returns:
        - RedirectResponse: A redirect response object that redirects the user to the '/docs' endpoint.
    Processing Logic:
        - Returns a RedirectResponse object.
        - The redirect URL is set to '/docs'.
        - The function is asynchronous.
        - No parameters are required.""""
    
    return RedirectResponse(url="/docs")


@app.post("/demands-raw", tags=["demands"], response_model=RawDemandsAnalysis)
async def analyze_raw_demands(
    scenario_file: UploadFile = File(...), consume_resources: bool = False
):
    """
    Analyze raw demands for a scenario. Raw demands describe the time and
    location of resources demanded by elements and/or missions.
    \f
    :param scenario_file: User input (scenario).
    :param consume_resources: True, if existing resources should be consumed.
    """
    # create a temp directory for working files
    with TemporaryDirectory() as tempdir:
        scenario_path = os.path.join(tempdir, scenario_file.filename)
        results_path = os.path.join(tempdir, "results.json")
        # write scenario file to temporary directory
        async with aiofiles.open(scenario_path, "wb") as new_scenario_file:
            content = await scenario_file.read()
            await new_scenario_file.write(content)
        # call spacenet headless script
        try:
            subprocess.check_output(
                [
                    "java",
                    "-jar",
                    spacenet_path,
                    "-h",
                    "demands-raw",
                    "-i",
                    scenario_path,
                    "-o",
                    results_path,
                    "-c" if consume_resources else "",
                ],
                stderr=subprocess.STDOUT,
                shell=False, universal_newlines=True,
                timeout=spacenet_timeout,
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=422, detail=e.output)
        except subprocess.TimeoutExpired as e:
            raise HTTPException(
                status_code=422, detail=f"Timeout exceeded ({spacenet_timeout} s)"
            )
        # read analysis outputs
        async with aiofiles.open(results_path, "r") as results_file:
            results = await results_file.read()
    return RawDemandsAnalysis.parse_raw(results)


@app.post("/demands-agg", tags=["demands"], response_model=AggregatedDemandsAnalysis)
async def analyze_aggregated_demands(
    scenario_file: UploadFile = File(...), consume_resources: bool = False
):
    """
    Analyze aggregated demands for a scenario. Aggregated demands group
    resources demanded by elements and/or missions to a time and node
    (supply node) or a start/end time and edge (supply edge).
    \f
    :param scenario_file: User input (scenario).
    :param consume_resources: True, if existing resources should be consumed.
    """
    # create a temp directory for working files
    with TemporaryDirectory() as tempdir:
        scenario_path = os.path.join(tempdir, scenario_file.filename)
        results_path = os.path.join(tempdir, "results.json")
        # write scenario file to temporary directory
        async with aiofiles.open(scenario_path, "wb") as new_scenario_file:
            content = await scenario_file.read()
            await new_scenario_file.write(content)
        # call spacenet headless script
        try:
            subprocess.check_output(
                [
                    "java",
                    "-jar",
                    spacenet_path,
                    "-h",
                    "demands-agg",
                    "-i",
                    scenario_path,
                    "-o",
                    results_path,
                    "-c" if consume_resources else "",
                ],
                stderr=subprocess.STDOUT,
                shell=False, universal_newlines=True,
                timeout=spacenet_timeout,
            )
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=422, detail=e.output)
        except subprocess.TimeoutExpired as e:
            raise HTTPException(
                status_code=422, detail=f"Timeout exceeded ({spacenet_timeout} s)"
            )
        # read analysis outputs
        async with aiofiles.open(results_path, "r") as results_file:
            results = await results_file.read()
    return AggregatedDemandsAnalysis.parse_raw(results)
