# CineLens - Movies At Your FingerTips

## Project Description

CineLens's goal is to help users find movies that are at the tip of your tongue! The user will be able to find a movie(s) through a still from the movie, a detailed description of a scene or the general synopsis.

## System Archiecture - High Level Overview

The project would consist of mainly two parts:
- Scene to Description: In the case the user uploads a scene from a movie, the first step would be to use an LLM/VLM to convert the scene to a text description of said scene.
- Description to Movie: Once a text description is obtained (either of the scene or the movie), an LLM will use RAG to query its database of movies to find a movie(s) that most closely match the given description and display to the user.

## Model Information

**LLaVA 1.5**

LLaVA 1.5 is a preconverted llamafile that has multi-modal capabilities that facilitates image-based chat.

**TinyLlama-1.1B**

TinyLlama is a model that has been pretrained on a 1.1B Llama model with 3 trillion tokens

## Timeline

### Week 1

- Define Project Description and Scope
- Set up GitHub Repository

### Week 2

- Explore different VLMs and LLMs 
- Finalize LLMs for pipeline
- Explore possible data sources for RAG System

### Week 3

- Convert LLMs to llamafile 
- Build out Scene to Description module

### Week 4

- Build out Description to Movie module
- Test entire pipeline

### Week 5 - 7

- Design the web application's UI
- Decide on archiecture for the web app
- Build & test web app

### Week 8 - 9

- Dockerize the web app
- Build and develop the CI/CD pipeline
- Test the pipeline

### Week 10 - 11

- Testing and submisson
