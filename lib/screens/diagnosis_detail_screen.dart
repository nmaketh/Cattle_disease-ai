import 'dart:io';
import 'package:flutter/material.dart';
import '../models/diagnosis_case.dart';

/// Screen showing detailed view of a past diagnosis
class DiagnosisDetailScreen extends StatelessWidget {
  final DiagnosisCase diagnosis;

  const DiagnosisDetailScreen({
    super.key,
    required this.diagnosis,
  });

  String _formatTimestamp(DateTime timestamp) {
    return '${timestamp.day}/${timestamp.month}/${timestamp.year} at ${timestamp.hour}:${timestamp.minute.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis Details'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Image
            Image.file(
              File(diagnosis.imagePath),
              height: 300,
              fit: BoxFit.cover,
              errorBuilder: (context, error, stackTrace) {
                return Container(
                  height: 300,
                  color: Colors.grey[300],
                  child: const Center(
                    child: Icon(Icons.broken_image, size: 64),
                  ),
                );
              },
            ),
            
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Disease name
                  Text(
                    diagnosis.diseaseName,
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                  ),
                  const SizedBox(height: 8),
                  
                  // Confidence
                  Row(
                    children: [
                      Icon(
                        diagnosis.confidence >= 0.7
                            ? Icons.check_circle
                            : Icons.warning,
                        color: diagnosis.confidence >= 0.7
                            ? Colors.green
                            : Colors.orange,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Confidence: ${(diagnosis.confidence * 100).toStringAsFixed(1)}%',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              color: diagnosis.confidence >= 0.7
                                  ? Colors.green
                                  : Colors.orange,
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  
                  // Timestamp
                  Row(
                    children: [
                      Icon(
                        Icons.access_time,
                        size: 16,
                        color: Colors.grey[600],
                      ),
                      const SizedBox(width: 4),
                      Text(
                        _formatTimestamp(diagnosis.timestamp),
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // Explanation section
                  Text(
                    'Explanation',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 8),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Text(
                        diagnosis.explanation,
                        style: Theme.of(context).textTheme.bodyMedium,
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // Additional info
                  if (diagnosis.confidence < 0.7)
                    Card(
                      color: Colors.orange[50],
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Row(
                          children: [
                            Icon(
                              Icons.info_outline,
                              color: Colors.orange[700],
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                'Low confidence prediction. Please consult a veterinarian for accurate diagnosis.',
                                style: TextStyle(
                                  color: Colors.orange[900],
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
