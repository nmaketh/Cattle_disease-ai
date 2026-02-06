# Developer Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Flutter SDK** (3.0.0 or higher)
  - Download from: https://flutter.dev/docs/get-started/install
- **Dart SDK** (included with Flutter)
- **Android Studio** (for Android development)
  - Download from: https://developer.android.com/studio
- **Xcode** (for iOS development, macOS only)
  - Available from Mac App Store
- **Git**

## Environment Setup

### 1. Install Flutter

Follow the official Flutter installation guide for your operating system:
- [Windows](https://flutter.dev/docs/get-started/install/windows)
- [macOS](https://flutter.dev/docs/get-started/install/macos)
- [Linux](https://flutter.dev/docs/get-started/install/linux)

### 2. Verify Installation

```bash
flutter doctor
```

This command checks your environment and displays a report. Fix any issues reported.

### 3. Clone the Repository

```bash
git clone https://github.com/nmaketh/Cattle_disease-ai.git
cd Cattle_disease-ai
```

### 4. Install Dependencies

```bash
flutter pub get
```

## Running the App

### On Android Emulator

1. Start an Android emulator from Android Studio
2. Run:
   ```bash
   flutter run
   ```

### On Android Physical Device

1. Enable Developer Options and USB Debugging on your device
2. Connect device via USB
3. Run:
   ```bash
   flutter run
   ```

### On iOS Simulator (macOS only)

1. Open iOS Simulator
2. Run:
   ```bash
   flutter run
   ```

### On iOS Physical Device (macOS only)

1. Connect your iPhone/iPad
2. Open the project in Xcode
3. Configure signing & capabilities
4. Run:
   ```bash
   flutter run
   ```

## Building for Release

### Android APK

```bash
flutter build apk --release
```

The APK will be at: `build/app/outputs/flutter-apk/app-release.apk`

### Android App Bundle

```bash
flutter build appbundle --release
```

### iOS

```bash
flutter build ios --release
```

Then open the project in Xcode to archive and upload to App Store.

## Project Structure

```
cattle_disease_ai/
├── android/              # Android-specific code
├── ios/                  # iOS-specific code
├── lib/                  # Dart application code
│   ├── main.dart        # App entry point
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── screens/         # UI screens
│   └── widgets/         # Reusable widgets
├── assets/              # Static assets
│   ├── models/          # ML models
│   └── images/          # Images
├── test/                # Unit and widget tests
├── pubspec.yaml         # Dependencies
└── README.md            # Documentation
```

## Development Workflow

### 1. Hot Reload

While the app is running, press `r` in the terminal to hot reload changes.

### 2. Hot Restart

Press `R` to hot restart the app (full restart).

### 3. Run Tests

```bash
flutter test
```

### 4. Analyze Code

```bash
flutter analyze
```

### 5. Format Code

```bash
flutter format lib/
```

## Adding a Real ML Model

The current implementation uses a sample ML service. To integrate a real model:

1. **Train your model** using TensorFlow/Keras
2. **Convert to TFLite:**
   ```python
   import tensorflow as tf
   
   # Load your trained model
   model = tf.keras.models.load_model('your_model.h5')
   
   # Convert to TFLite
   converter = tf.lite.TFLiteConverter.from_keras_model(model)
   tflite_model = converter.convert()
   
   # Save the model
   with open('cattle_disease_model.tflite', 'wb') as f:
       f.write(tflite_model)
   ```

3. **Place the model** in `assets/models/`

4. **Update ml_service.dart:**
   ```dart
   import 'package:tflite_flutter/tflite_flutter.dart';
   
   // Load model
   interpreter = await Interpreter.fromAsset('assets/models/cattle_disease_model.tflite');
   
   // Run inference
   interpreter.run(input, output);
   ```

## Troubleshooting

### Issue: "flutter: command not found"
**Solution:** 
Flutter is not installed or not in your PATH.
1. Install Flutter from https://flutter.dev/docs/get-started/install
2. Add Flutter to your PATH (see installation guide)
3. Restart your terminal/command prompt
4. Verify with: `flutter --version`

### Issue: "Flutter SDK not found"
**Solution:** Ensure Flutter is in your PATH and run `flutter doctor`

### Issue: Camera not working in emulator
**Solution:** Use a physical device for camera functionality

### Issue: Dependencies conflict
**Solution:** Run `flutter pub upgrade` and `flutter clean`

### Issue: Build fails
**Solution:** 
```bash
flutter clean
flutter pub get
flutter run
```

## Database Schema

The app uses SQLite with the following schema:

```sql
CREATE TABLE diagnoses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  imagePath TEXT NOT NULL,
  diseaseName TEXT NOT NULL,
  confidence REAL NOT NULL,
  explanation TEXT NOT NULL,
  timestamp TEXT NOT NULL
);
```

## Key Dependencies

- `tflite_flutter`: TensorFlow Lite inference
- `sqflite`: SQLite database
- `image_picker`: Camera and gallery access
- `path_provider`: File system access
- `image`: Image processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Best Practices

- Follow the [Effective Dart](https://dart.dev/guides/language/effective-dart) style guide
- Write tests for new features
- Keep widgets small and focused
- Use const constructors when possible
- Comment complex logic

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues first
- Provide clear reproduction steps

## Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Documentation](https://dart.dev/guides)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
- [Material Design](https://material.io/design)
