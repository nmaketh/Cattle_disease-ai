import 'dart:io';
import 'package:flutter/material.dart';
import '../models/diagnosis_case.dart';
import '../models/disease_prediction.dart';
import '../services/image_service.dart';
import '../services/ml_service.dart';
import '../services/database_service.dart';
import '../widgets/prediction_card.dart';

/// Screen for capturing image and running diagnosis
class DiagnosisScreen extends StatefulWidget {
  const DiagnosisScreen({super.key});

  @override
  State<DiagnosisScreen> createState() => _DiagnosisScreenState();
}

class _DiagnosisScreenState extends State<DiagnosisScreen> {
  String? _imagePath;
  DiseasePrediction? _prediction;
  bool _isProcessing = false;

  final ImageService _imageService = ImageService.instance;
  final MLService _mlService = MLService.instance;
  final DatabaseService _dbService = DatabaseService.instance;

  @override
  void initState() {
    super.initState();
    _initializeML();
  }

  Future<void> _initializeML() async {
    await _mlService.loadModel();
  }

  Future<void> _captureImage(ImageSource source) async {
    String? imagePath;
    
    if (source == ImageSource.camera) {
      imagePath = await _imageService.captureFromCamera();
    } else {
      imagePath = await _imageService.pickFromGallery();
    }

    if (imagePath != null) {
      setState(() {
        _imagePath = imagePath;
        _prediction = null;
      });
    }
  }

  Future<void> _runDiagnosis() async {
    if (_imagePath == null) return;

    setState(() {
      _isProcessing = true;
    });

    try {
      final prediction = await _mlService.predict(_imagePath!);
      
      setState(() {
        _prediction = prediction;
        _isProcessing = false;
      });
    } catch (e) {
      setState(() {
        _isProcessing = false;
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error running diagnosis: $e')),
        );
      }
    }
  }

  Future<void> _saveDiagnosis() async {
    if (_imagePath == null || _prediction == null) return;

    try {
      final diagnosisCase = DiagnosisCase(
        imagePath: _imagePath!,
        diseaseName: _prediction!.diseaseName,
        confidence: _prediction!.confidence,
        explanation: _prediction!.explanation,
        timestamp: DateTime.now(),
      );

      await _dbService.insertDiagnosis(diagnosisCase);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Diagnosis saved to history'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error saving diagnosis: $e')),
        );
      }
    }
  }

  void _showImageSourceDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Select Image Source'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Camera'),
              onTap: () {
                Navigator.pop(context);
                _captureImage(ImageSource.camera);
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Gallery'),
              onTap: () {
                Navigator.pop(context);
                _captureImage(ImageSource.gallery);
              },
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New Diagnosis'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          if (_prediction != null)
            IconButton(
              icon: const Icon(Icons.save),
              onPressed: _saveDiagnosis,
              tooltip: 'Save to history',
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Image display
            if (_imagePath != null)
              Card(
                clipBehavior: Clip.antiAlias,
                child: Image.file(
                  File(_imagePath!),
                  height: 300,
                  fit: BoxFit.cover,
                ),
              )
            else
              Card(
                child: Container(
                  height: 300,
                  alignment: Alignment.center,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.add_photo_alternate,
                        size: 64,
                        color: Colors.grey[400],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No image selected',
                        style: TextStyle(
                          color: Colors.grey[600],
                          fontSize: 16,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 16),

            // Capture button
            ElevatedButton.icon(
              onPressed: _showImageSourceDialog,
              icon: const Icon(Icons.camera_alt),
              label: Text(_imagePath == null ? 'Capture Image' : 'Change Image'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
            const SizedBox(height: 16),

            // Analyze button
            if (_imagePath != null && _prediction == null)
              ElevatedButton.icon(
                onPressed: _isProcessing ? null : _runDiagnosis,
                icon: _isProcessing
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Icon(Icons.analytics),
                label: Text(_isProcessing ? 'Analyzing...' : 'Run Diagnosis'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  foregroundColor: Colors.white,
                ),
              ),

            // Prediction results
            if (_prediction != null) ...[
              const SizedBox(height: 24),
              PredictionCard(prediction: _prediction!),
            ],
          ],
        ),
      ),
    );
  }
}

enum ImageSource { camera, gallery }
