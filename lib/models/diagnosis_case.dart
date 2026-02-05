/// Model representing a cattle disease diagnosis case
class DiagnosisCase {
  final int? id;
  final String imagePath;
  final String diseaseName;
  final double confidence;
  final String explanation;
  final DateTime timestamp;

  DiagnosisCase({
    this.id,
    required this.imagePath,
    required this.diseaseName,
    required this.confidence,
    required this.explanation,
    required this.timestamp,
  });

  /// Convert DiagnosisCase to Map for database storage
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'imagePath': imagePath,
      'diseaseName': diseaseName,
      'confidence': confidence,
      'explanation': explanation,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  /// Create DiagnosisCase from Map (database record)
  factory DiagnosisCase.fromMap(Map<String, dynamic> map) {
    return DiagnosisCase(
      id: map['id'] as int?,
      imagePath: map['imagePath'] as String,
      diseaseName: map['diseaseName'] as String,
      confidence: map['confidence'] as double,
      explanation: map['explanation'] as String,
      timestamp: DateTime.parse(map['timestamp'] as String),
    );
  }

  /// Copy with method for creating modified copies
  DiagnosisCase copyWith({
    int? id,
    String? imagePath,
    String? diseaseName,
    double? confidence,
    String? explanation,
    DateTime? timestamp,
  }) {
    return DiagnosisCase(
      id: id ?? this.id,
      imagePath: imagePath ?? this.imagePath,
      diseaseName: diseaseName ?? this.diseaseName,
      confidence: confidence ?? this.confidence,
      explanation: explanation ?? this.explanation,
      timestamp: timestamp ?? this.timestamp,
    );
  }
}
