# Phishing Detection System

A machine-learning-based URL phishing detection system that combines a Random Forest classifier with heuristic risk signals to classify URLs and generate a risk score.

## Overview

The system analyzes submitted URLs and produces:

- A phishing probability from the machine-learning model
- An IP address risk indicator
- A keyword-based risk indicator
- A combined risk score from 0–100
- A final classification of `PHISHING` or `SAFE`

The project was developed as an educational cybersecurity application to explore machine learning, URL-based phishing detection, and risk scoring.

## Architecture

```text
User submits URL
       ↓
Feature extraction
       ↓
13 URL-based features
       ↓
Random Forest model
       ↓
ML phishing probability
       ↓
Hybrid risk engine
       ↓
Risk score + final classification
       ↓
Web interface