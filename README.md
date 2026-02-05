# Cattle Disease AI - Offline Mobile Diagnostic App

An offline-first Flutter mobile application for early cattle disease diagnosis using on-device AI and TensorFlow Lite.

## Features

✨ **Key Features:**
- 📸 Capture cattle images using camera or select from gallery
- 🤖 On-device TensorFlow Lite inference (no internet required)
- 📊 Disease prediction with confidence scores and detailed explanations
- 💾 Local SQLite database for storing diagnosis history
- 📜 Browse and manage past diagnoses
- 🎨 Clean, intuitive Material Design UI
- 🔧 Modular architecture for easy maintenance and extension

## Supported Diseases

The app is designed to detect the following cattle diseases:
1. **Healthy** - Normal, healthy cattle
2. **Foot and Mouth Disease** - Highly contagious viral disease
3. **Lumpy Skin Disease** - Viral disease causing skin nodules
4. **Mastitis** - Inflammation of the mammary gland
5. **Pink Eye** - Infectious bacterial conjunctivitis

## Architecture

```
lib/
├── main.dart                 # App entry point
├── models/                   # Data models
│   ├── diagnosis_case.dart   # Diagnosis record model
│   └── disease_prediction.dart # Prediction result model
├── services/                 # Business logic services
│   ├── database_service.dart # SQLite database operations
│   ├── image_service.dart    # Image capture and storage
│   └── ml_service.dart       # TensorFlow Lite inference
├── screens/                  # UI screens
│   ├── home_screen.dart      # Main landing screen
│   ├── diagnosis_screen.dart # Image capture & analysis
│   ├── history_screen.dart   # Past diagnoses list
│   └── diagnosis_detail_screen.dart # Detailed diagnosis view
└── widgets/                  # Reusable UI components
    └── prediction_card.dart  # Prediction results display
```

## Getting Started

### Prerequisites

- Flutter SDK (3.0.0 or higher)
- Dart SDK (included with Flutter)
- Android Studio / Xcode for mobile development
- A physical device or emulator

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nmaketh/Cattle_disease-ai.git
   cd Cattle_disease-ai
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Run the app:**
   ```bash
   flutter run
   ```

### Adding Your Own ML Model

The current implementation includes a sample ML service for demonstration. To use a real trained model:

1. Train your TensorFlow model for cattle disease classification
2. Convert it to TensorFlow Lite format (.tflite)
3. Place the model file in `assets/models/cattle_disease_model.tflite`
4. Update `ml_service.dart` to load and use the actual model

See `assets/models/README.md` for detailed instructions.

## Dependencies

- **flutter**: UI framework
- **tflite_flutter**: TensorFlow Lite integration
- **sqflite**: Local SQLite database
- **path_provider**: Access to device file system
- **image_picker**: Camera and gallery access
- **image**: Image processing utilities

## How It Works

1. **Image Capture**: User captures or selects a cattle image
2. **Preprocessing**: Image is resized and normalized for model input
3. **Inference**: TensorFlow Lite model runs on-device to predict disease
4. **Results Display**: Prediction shown with confidence, symptoms, and recommendations
5. **Storage**: User can save diagnosis to local SQLite database
6. **History**: Access and manage past diagnoses offline

## Offline-First Design

This app is designed to work completely offline:
- ✅ ML inference runs entirely on-device
- ✅ All data stored locally using SQLite
- ✅ Images saved to local storage
- ✅ No internet connection required

## Screenshots

_(Screenshots would go here when the app is built)_

## Future Enhancements

- [ ] Export diagnosis reports as PDF
- [ ] Multi-language support
- [ ] Advanced image preprocessing
- [ ] Multiple disease detection in single image
- [ ] Integration with veterinary databases
- [ ] Cloud sync option for backup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This application is for educational and informational purposes only. It should not replace professional veterinary diagnosis and treatment. Always consult a qualified veterinarian for accurate diagnosis and treatment of cattle diseases.

## Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Flutter and TensorFlow Lite**