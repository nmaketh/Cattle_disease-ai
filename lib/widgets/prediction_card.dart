import 'package:flutter/material.dart';
import '../models/disease_prediction.dart';

/// Widget displaying disease prediction results
class PredictionCard extends StatelessWidget {
  final DiseasePrediction prediction;

  const PredictionCard({
    super.key,
    required this.prediction,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              children: [
                Icon(
                  prediction.isReliable
                      ? Icons.check_circle
                      : Icons.warning,
                  color: prediction.isReliable
                      ? Colors.green
                      : Colors.orange,
                  size: 32,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        prediction.diseaseName,
                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.bold,
                              color: Theme.of(context).colorScheme.primary,
                            ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Confidence: ${prediction.confidencePercentage}',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              color: prediction.isReliable
                                  ? Colors.green
                                  : Colors.orange,
                              fontWeight: FontWeight.bold,
                            ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(),
            const SizedBox(height: 16),
            
            // Explanation
            Text(
              'Explanation',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              prediction.explanation,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            
            // Symptoms
            if (prediction.symptoms.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Common Symptoms',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              ...prediction.symptoms.map(
                (symptom) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.fiber_manual_record, size: 8),
                      const SizedBox(width: 8),
                      Expanded(child: Text(symptom)),
                    ],
                  ),
                ),
              ),
            ],
            
            // Recommendations
            if (prediction.recommendations.isNotEmpty) ...[
              const SizedBox(height: 16),
              Text(
                'Recommendations',
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              ...prediction.recommendations.map(
                (recommendation) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(
                        Icons.check,
                        size: 16,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 8),
                      Expanded(child: Text(recommendation)),
                    ],
                  ),
                ),
              ),
            ],
            
            // Warning for low confidence
            if (!prediction.isReliable) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.orange[50],
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.orange),
                ),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.orange[700]),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Low confidence prediction. Please consult a veterinarian for accurate diagnosis.',
                        style: TextStyle(
                          color: Colors.orange[900],
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
