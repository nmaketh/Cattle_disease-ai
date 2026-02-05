# Architecture Documentation

## Application Architecture

This application follows a **clean, modular architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────┐
│                   UI Layer                      │
│  ┌──────────────────────────────────────────┐  │
│  │          Screens & Widgets               │  │
│  │  - HomeScreen                            │  │
│  │  - DiagnosisScreen                       │  │
│  │  - HistoryScreen                         │  │
│  │  - DiagnosisDetailScreen                 │  │
│  │  - PredictionCard (widget)               │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│                Business Logic                   │
│  ┌──────────────────────────────────────────┐  │
│  │              Services                    │  │
│  │  - MLService (TFLite inference)          │  │
│  │  - DatabaseService (SQLite)              │  │
│  │  - ImageService (Camera/Gallery)         │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│                  Data Layer                     │
│  ┌──────────────────────────────────────────┐  │
│  │               Models                     │  │
│  │  - DiagnosisCase                         │  │
│  │  - DiseasePrediction                     │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│              Storage & Hardware                 │
│  - SQLite Database                              │
│  - Local File System                            │
│  - Camera/Gallery                               │
│  - TensorFlow Lite Runtime                      │
└─────────────────────────────────────────────────┘
```

## Design Patterns

### 1. Singleton Pattern
Used for services to ensure single instance:
- `DatabaseService.instance`
- `MLService.instance`
- `ImageService.instance`

### 2. Repository Pattern
`DatabaseService` acts as a repository for diagnosis data, abstracting data access.

### 3. Service Pattern
Business logic is encapsulated in service classes, keeping UI components clean.

### 4. Model-View Pattern
- **Models**: Data structures (DiagnosisCase, DiseasePrediction)
- **Views**: UI screens and widgets
- **Services**: Bridge between models and views

## Data Flow

### Diagnosis Flow
```
User captures image
    ↓
ImageService saves image
    ↓
MLService processes image
    ↓
Preprocesses (resize, normalize)
    ↓
Runs TFLite inference
    ↓
Returns DiseasePrediction
    ↓
UI displays results
    ↓
User saves diagnosis
    ↓
DatabaseService stores DiagnosisCase
    ↓
Saved to SQLite
```

### History Flow
```
User opens history
    ↓
DatabaseService.getAllDiagnoses()
    ↓
Retrieves from SQLite
    ↓
Converts to DiagnosisCase models
    ↓
UI displays list
    ↓
User taps item
    ↓
Shows DiagnosisDetailScreen
```

## Component Details

### Services

#### MLService
- **Purpose**: Handle ML inference using TensorFlow Lite
- **Key Methods**:
  - `loadModel()`: Initialize TFLite interpreter
  - `predict(imagePath)`: Run inference on image
  - `_preprocessImage()`: Resize and normalize image
  - `_runInference()`: Execute model prediction
- **Dependencies**: tflite_flutter, image processing

#### DatabaseService
- **Purpose**: Manage local SQLite database
- **Key Methods**:
  - `insertDiagnosis()`: Save new diagnosis
  - `getAllDiagnoses()`: Retrieve all diagnoses
  - `getDiagnosis(id)`: Get specific diagnosis
  - `deleteDiagnosis(id)`: Remove diagnosis
- **Dependencies**: sqflite, path

#### ImageService
- **Purpose**: Handle image capture and storage
- **Key Methods**:
  - `captureFromCamera()`: Take photo with camera
  - `pickFromGallery()`: Select from gallery
  - `deleteImage()`: Remove image file
- **Dependencies**: image_picker, path_provider

### Models

#### DiagnosisCase
- Represents a complete diagnosis record
- Stored in SQLite database
- Fields: id, imagePath, diseaseName, confidence, explanation, timestamp

#### DiseasePrediction
- Represents ML model output
- Contains disease information and recommendations
- Fields: diseaseName, confidence, explanation, symptoms, recommendations

### Screens

#### HomeScreen
- Main landing page
- Navigation hub to other screens
- Shows app description

#### DiagnosisScreen
- Capture/select image
- Run ML inference
- Display prediction results
- Save to history

#### HistoryScreen
- List all past diagnoses
- Delete diagnoses
- Navigate to details

#### DiagnosisDetailScreen
- Show detailed diagnosis information
- Display image and all metadata

## Offline-First Design

The app is designed to work completely offline:

1. **ML Inference**: TensorFlow Lite runs on-device
2. **Data Storage**: SQLite database stored locally
3. **Image Storage**: Images saved to app's documents directory
4. **No Network Calls**: All processing happens locally

## State Management

Currently using **StatefulWidget** for simple state management:
- Local state in each screen
- Service instances shared via Singleton pattern

For larger apps, consider:
- Provider
- Riverpod
- BLoC pattern

## Error Handling

- Try-catch blocks in all async operations
- User-friendly error messages via SnackBars
- Fallback UI for missing images
- Graceful degradation when model fails

## Security Considerations

- Local data only (no cloud sync)
- No sensitive data stored
- Permissions requested: Camera, Storage
- Image data stays on device

## Performance Optimizations

- Image compression before storage
- Lazy loading in history list
- Efficient database queries
- Model inference optimized for mobile

## Testing Strategy

- Widget tests for UI components
- Unit tests for services
- Integration tests for flows
- Manual testing on devices

## Future Enhancements

1. **State Management**: Implement Provider/BLoC
2. **Caching**: Cache ML results
3. **Export**: PDF report generation
4. **Sync**: Optional cloud backup
5. **Multi-language**: i18n support
6. **Accessibility**: Screen reader support
7. **Analytics**: Usage tracking (offline)
