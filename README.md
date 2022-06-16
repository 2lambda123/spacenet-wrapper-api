# SpaceNet Wrapper API

This project provides a thin Python-based wrapper API that exposes SpaceNet
Java analysis capabilities as a RESTful HTTP service.

## Installation

1. Install the minimal required Python dependencies with the shell command:
```
pip install -r requirements.txt
```

2. Create a `.env` file in this directory, and specify the location of your
SpaceNet Java Archive (JAR) file. For example (on Mac/Linux):
```
SPACENET_PATH = /your/path/to/spacenet-2.5.1464-jar-with-dependencies.jar
```
or (on Windows):
```
SPACENET_PATH = C:\your\path\to\spacenet-2.5.1464-jar-with-dependencies.jar
```

## Usage

Start the application with the shell command:
```
uvicorn app.main:app --reload
```
the API service is available at <http://localhost:8000/docs>.

Upload scenario files (.json or .xml) to view demands analysis results.

## Contact

Paul T. Grogan  <paul@ptgrogan.com>

## License

Copyright 2022 Paul T. Grogan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
