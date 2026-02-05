import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import '../models/diagnosis_case.dart';

/// Service for managing local SQLite database operations
class DatabaseService {
  static final DatabaseService instance = DatabaseService._init();
  static Database? _database;

  DatabaseService._init();

  /// Get database instance, creating it if necessary
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('cattle_diagnoses.db');
    return _database!;
  }

  /// Initialize database
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  /// Create database tables
  Future<void> _createDB(Database db, int version) async {
    const idType = 'INTEGER PRIMARY KEY AUTOINCREMENT';
    const textType = 'TEXT NOT NULL';
    const realType = 'REAL NOT NULL';

    await db.execute('''
      CREATE TABLE diagnoses (
        id $idType,
        imagePath $textType,
        diseaseName $textType,
        confidence $realType,
        explanation $textType,
        timestamp $textType
      )
    ''');
  }

  /// Insert a new diagnosis case
  Future<DiagnosisCase> insertDiagnosis(DiagnosisCase diagnosis) async {
    final db = await instance.database;
    final id = await db.insert('diagnoses', diagnosis.toMap());
    return diagnosis.copyWith(id: id);
  }

  /// Get all diagnosis cases, ordered by timestamp (newest first)
  Future<List<DiagnosisCase>> getAllDiagnoses() async {
    final db = await instance.database;
    const orderBy = 'timestamp DESC';
    final result = await db.query('diagnoses', orderBy: orderBy);
    return result.map((map) => DiagnosisCase.fromMap(map)).toList();
  }

  /// Get a specific diagnosis by ID
  Future<DiagnosisCase?> getDiagnosis(int id) async {
    final db = await instance.database;
    final maps = await db.query(
      'diagnoses',
      where: 'id = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty) {
      return DiagnosisCase.fromMap(maps.first);
    }
    return null;
  }

  /// Delete a diagnosis by ID
  Future<int> deleteDiagnosis(int id) async {
    final db = await instance.database;
    return await db.delete(
      'diagnoses',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  /// Delete all diagnoses
  Future<int> deleteAllDiagnoses() async {
    final db = await instance.database;
    return await db.delete('diagnoses');
  }

  /// Close database connection
  Future<void> close() async {
    final db = await instance.database;
    await db.close();
  }
}
