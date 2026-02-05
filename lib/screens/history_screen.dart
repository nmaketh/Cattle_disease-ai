import 'dart:io';
import 'package:flutter/material.dart';
import '../models/diagnosis_case.dart';
import '../services/database_service.dart';
import 'diagnosis_detail_screen.dart';

/// Screen displaying history of past diagnoses
class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  final DatabaseService _dbService = DatabaseService.instance;
  List<DiagnosisCase> _diagnoses = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadDiagnoses();
  }

  Future<void> _loadDiagnoses() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final diagnoses = await _dbService.getAllDiagnoses();
      setState(() {
        _diagnoses = diagnoses;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading history: $e')),
        );
      }
    }
  }

  Future<void> _deleteDiagnosis(DiagnosisCase diagnosis) async {
    if (diagnosis.id == null) return;

    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Diagnosis'),
        content: const Text('Are you sure you want to delete this diagnosis?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await _dbService.deleteDiagnosis(diagnosis.id!);
        await _loadDiagnoses();
        
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Diagnosis deleted'),
              backgroundColor: Colors.orange,
            ),
          );
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error deleting diagnosis: $e')),
          );
        }
      }
    }
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inDays == 0) {
      if (difference.inHours == 0) {
        if (difference.inMinutes == 0) {
          return 'Just now';
        }
        return '${difference.inMinutes} minutes ago';
      }
      return '${difference.inHours} hours ago';
    } else if (difference.inDays == 1) {
      return 'Yesterday';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} days ago';
    } else {
      return '${timestamp.day}/${timestamp.month}/${timestamp.year}';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnosis History'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          if (_diagnoses.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.refresh),
              onPressed: _loadDiagnoses,
              tooltip: 'Refresh',
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _diagnoses.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.history,
                        size: 64,
                        color: Colors.grey[400],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No diagnosis history',
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.grey[600],
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Run a diagnosis to see results here',
                        style: TextStyle(
                          color: Colors.grey[500],
                        ),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(8),
                  itemCount: _diagnoses.length,
                  itemBuilder: (context, index) {
                    final diagnosis = _diagnoses[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      child: ListTile(
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.file(
                            File(diagnosis.imagePath),
                            width: 60,
                            height: 60,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return Container(
                                width: 60,
                                height: 60,
                                color: Colors.grey[300],
                                child: const Icon(Icons.broken_image),
                              );
                            },
                          ),
                        ),
                        title: Text(
                          diagnosis.diseaseName,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const SizedBox(height: 4),
                            Text(
                              'Confidence: ${(diagnosis.confidence * 100).toStringAsFixed(1)}%',
                              style: TextStyle(
                                color: diagnosis.confidence >= 0.7
                                    ? Colors.green
                                    : Colors.orange,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              _formatTimestamp(diagnosis.timestamp),
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey[600],
                              ),
                            ),
                          ],
                        ),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => _deleteDiagnosis(diagnosis),
                        ),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) =>
                                  DiagnosisDetailScreen(diagnosis: diagnosis),
                            ),
                          );
                        },
                      ),
                    );
                  },
                ),
    );
  }
}
