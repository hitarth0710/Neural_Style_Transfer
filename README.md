# ArtStyle AI - Neural Style Transfer Web Application

A powerful web application that transforms ordinary photos into artistic masterpieces using neural style transfer technology powered by Stable Diffusion.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Overview

ArtStyle AI is a Flask-based web application that allows users to upload content images and apply artistic styles to them using neural style transfer techniques. The application leverages Stable Diffusion's powerful image generation capabilities to create high-quality artistic transformations.

## Features

- **User Authentication System**: Register, login, and manage your profile
- **Style Transfer**: Upload content and style images to create artistic transformations
- **Style Prompt Support**: Use text prompts to further guide the style transfer process
- **Style Strength Adjustment**: Control the intensity of the style application
- **Personal Gallery**: View, manage, and download your style transfer creations
- **User Dashboard**: Track usage statistics and view recent creations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Neural Networks**: Stable Diffusion (via diffusers library)
- **Image Processing**: PIL (Python Imaging Library)
- **Deployment**: Migrations handled with Alembic/Flask-Migrate

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/neural_style_transfer.git
   cd neural_style_transfer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create a .env file with the following variables
   SECRET_KEY=your_secret_key
   DATABASE_URI=sqlite:///site.db
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

## Usage

1. **Register/Login**: Create an account or log in to access the full features
2. **Upload Images**: Select a content image and a style image
3. **Customize Settings**: Adjust style strength and add optional text prompts
4. **Generate**: Process the images to create your stylized result
5. **View Results**: See the transformation and download the result
6. **Manage Gallery**: View all your past creations in your personal gallery

## Project Structure

```
neural_style_transfer/
├── app/
│   ├── auth/                  # Authentication-related routes and forms
│   ├── static/                # Static files (CSS, JS, images)
│   │   ├── css/               # CSS stylesheets
│   │   ├── img/               # Image assets
│   │   ├── uploads/           # User uploaded images
│   │   └── results/           # Style transfer results
│   ├── style_transfer/        # Style transfer functionality
│   │   ├── forms.py           # Form definitions
│   │   ├── models.py          # Database models
│   │   ├── routes.py          # Route handlers
│   │   └── utils.py           # Utility functions for style transfer
│   ├── templates/             # HTML templates
│   │   ├── auth/              # Authentication templates
│   │   └── style_transfer/    # Style transfer templates
│   ├── __init__.py            # App initialization
│   └── models.py              # Database models
├── migrations/                # Database migration files
├── run.py                     # Application entry point
└── requirements.txt           # Project dependencies
```

## Screenshots

![image](https://github.com/user-attachments/assets/91962bd8-eb6f-4cb2-a8d3-b528f45cd5b0)
![image](https://github.com/user-attachments/assets/af138de5-e0a2-4ec6-9bcb-6f3bb0c1292e)
![image](https://github.com/user-attachments/assets/3fa9a97d-bfb2-444f-b903-d098e58ed599)
![image](https://github.com/user-attachments/assets/9a1b7680-6481-411c-8719-abe6d28fee3f)
![image](https://github.com/user-attachments/assets/cdf9faf0-80db-4de5-8423-77638b0b78af)



Example sections to include:

- Home Page
- Style Transfer Interface
- Results Page
- User Gallery
- User Profile Dashboard

## Future Enhancements

- Favorite styles system
- Sharing creations on social media
- Additional style transfer algorithms
- Batch processing for multiple images
- Premium features for subscribed users
- Mobile application

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---
