/// Model representing a disease prediction result
class DiseasePrediction {
  final String diseaseName;
  final double confidence;
  final String explanation;
  final List<String> symptoms;
  final List<String> recommendations;

  DiseasePrediction({
    required this.diseaseName,
    required this.confidence,
    required this.explanation,
    this.symptoms = const [],
    this.recommendations = const [],
  });

  /// Get confidence as percentage string
  String get confidencePercentage => '${(confidence * 100).toStringAsFixed(1)}%';

  /// Check if confidence is high enough to be reliable
  bool get isReliable => confidence >= 0.7;
}
