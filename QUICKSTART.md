# Quick Start Guide

Get up and running with Cattle Disease AI in minutes!

## Prerequisites

- Flutter SDK 3.0.0+
- Android Studio or Xcode
- Git

## Installation (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/nmaketh/Cattle_disease-ai.git
cd Cattle_disease-ai

# 2. Install dependencies
flutter pub get

# 3. Run the app
flutter run
```

That's it! The app should now be running on your device/emulator.

## First Steps

### 1. Launch the App
You'll see the home screen with two main buttons.

### 2. Try a Diagnosis
- Tap **"New Diagnosis"**
- Tap **"Capture Image"**
- Choose **Camera** or **Gallery**
- Select or take a cattle image
- Tap **"Run Diagnosis"**
- View the prediction results
- Tap the **save icon** (💾) to save

### 3. View History
- Go back to home
- Tap **"Diagnosis History"**
- See all your saved diagnoses
- Tap any item for details

## What's Included

✅ **Complete Flutter App** - Ready to build and deploy  
✅ **Offline ML Service** - Sample TensorFlow Lite integration  
✅ **SQLite Database** - Local data persistence  
✅ **Image Handling** - Camera and gallery support  
✅ **Clean UI** - Material Design 3  
✅ **5 Disease Classes** - Pre-configured disease information  

## Sample Mode

⚠️ **Note**: The app currently runs in **sample mode** with a simulated ML model. This demonstrates the architecture and user flow.

To use a real model:
1. Train or obtain a TensorFlow Lite model
2. Place it in `assets/models/cattle_disease_model.tflite`
3. Update `lib/services/ml_service.dart` to load the actual model

See `SETUP.md` for detailed instructions.

## Project Structure

```
├── lib/
│   ├── main.dart              # App entry point
│   ├── models/                # Data models
│   ├── services/              # Business logic
│   ├── screens/               # UI screens
│   └── widgets/               # Reusable widgets
├── assets/
│   └── models/                # ML models go here
├── test/                      # Tests
└── README.md                  # Full documentation
```

## Key Features

🎯 **Diagnosis Flow**
- Capture image → Analyze → View results → Save

🗄️ **Data Management**
- All stored locally in SQLite
- No internet required

🤖 **ML Integration**
- TensorFlow Lite ready
- On-device inference
- Fast predictions

## Common Commands

```bash
# Run app
flutter run

# Run tests
flutter test

# Check code
flutter analyze

# Format code
flutter format lib/

# Build APK
flutter build apk --release

# Clean build
flutter clean && flutter pub get
```

## Need Help?

📖 **Full Documentation**: See README.md  
🔧 **Setup Issues**: See SETUP.md  
👥 **User Guide**: See USER_GUIDE.md  
🏗️ **Architecture**: See ARCHITECTURE.md  
🤝 **Contributing**: See CONTRIBUTING.md  

## Quick Tips

💡 Use a physical device for camera testing  
💡 Check permissions in device settings  
💡 Sample mode works without a real ML model  
💡 All data stays on your device  

## Next Steps

1. ✅ Run the app successfully
2. 📸 Try capturing images
3. 🔍 Explore the UI and features
4. 🧪 Run tests: `flutter test`
5. 📱 Build release APK
6. 🤖 Add your own ML model
7. 🚀 Deploy to users

## Troubleshooting

**App won't build?**
```bash
flutter clean
flutter pub get
flutter run
```

**Dependencies error?**
```bash
flutter pub upgrade
```

**Camera not working?**
- Use a physical device
- Check camera permissions

## Support

- 🐛 Issues: https://github.com/nmaketh/Cattle_disease-ai/issues
- 💬 Discussions: GitHub Discussions
- 📧 Contact: Open an issue

---

**Ready to start?** Run `flutter run` and begin diagnosing! 🐄🤖
