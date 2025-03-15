# G-CODE Editor

A modern, user-friendly interface for editing and processing G-CODE files, designed for CNC and manufacturing applications.

![G-CODE Editor](https://res.cloudinary.com/mustafakbaser/image/upload/v1742032395/G-Code_ihfc01.png)

## Overview

G-CODE Editor is a sophisticated application built with PyQt5 that provides a comprehensive environment for managing G-CODE operations. It follows the Model-View-Controller (MVC) design pattern for maintainable and extensible code architecture.

## Features

- **Modern Interface**: Clean, intuitive UI with light theme and responsive controls
- **Parameter Management**: Easy editing of G-CODE parameters with real-time updates
- **Route Processing**: Load and process multiple route files with coordinate calibration
- **Thread Cutting Controls**: Specialized parameters for thread cutting operations
- **Punteriz Settings**: Configure stitch start and end settings
- **Speed Control**: Dynamic speed adjustment with acceleration and deceleration profiles
- **Multilingual Support**: Full interface available in both Turkish and English
- **Automatic File Management**: Organized handling of route files and G-CODE output

## Project Structure

The application is organized following the MVC architecture:

- **models/**: Data and business logic
  - `gcode_model.py`: Main model for G-CODE data management
  - `gcode_processor.py`: Processor for G-CODE operations
  - `multi_route_processor.py`: Handles multiple route processing

- **views/**: User interface components
  - `main_view.py`: Main application window and UI elements

- **controllers/**: Application logic
  - `main_controller.py`: Connects models and views, handles user interactions

- **utils/**: Helper utilities
  - `styles.py`: UI styling and theme management
  - `language.py`: Multilingual support

## Installation

1. Ensure you have Python 3.6+ installed on your system
2. Clone the repository or download the source code
```
git clone https://github.com/mustafakbaser/G-CODE-Editor.git
```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```
   
   Alternatively, use the provided `run_app.bat` file on Windows systems.

## Usage Guide

### Setting Parameters

1. **G-Code Start Parameters**: Define initialization parameters
2. **Route Start Parameters**: Configure parameters for route beginnings
3. **Thread Cut Parameters**: Set thread cutting specifications
4. **G-Code End Parameters**: Define closing operations

### Machine Configuration

1. **Needle Positions**: Set needle down and up positions
2. **Speed Control**: Configure starting speed, maximum speed, and acceleration
3. **Calibration Values**: Set X and Y calibration values for precise positioning

### File Operations

1. **Loading Files**: Click "Load File" to import route files from the "routes" folder
2. **Generating G-CODE**: Click "Generate G-CODE" to process loaded routes with current parameters
3. **Saving Files**: Click "Save File" to export the generated G-CODE to the "gcode_output" folder

### Language Settings

- Switch between Turkish and English using the Language menu
- All UI elements, messages, and dialogs will update immediately to the selected language

## Folder Structure

- **routes/**: Contains route files (.nc) for processing
- **gcode_output/**: Destination for generated G-CODE files
- **parameters.json**: Stores default and user-defined parameters

## Development Notes

This application is designed for manufacturing environments where precision and reliability are essential. The code structure emphasizes maintainability and extensibility, allowing for future enhancements.

Key technical aspects:
- PyQt5 for responsive UI components
- JSON-based parameter storage
- Dynamic language switching
- Modular processing pipeline

## Requirements

- Python 3.6+
- PyQt5
- Additional dependencies listed in requirements.txt