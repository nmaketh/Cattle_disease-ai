import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as path;

/// Service for handling image capture and storage
class ImageService {
  static final ImageService instance = ImageService._init();
  final ImagePicker _picker = ImagePicker();

  ImageService._init();

  /// Capture image from camera
  Future<String?> captureFromCamera() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.camera,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );

      if (image != null) {
        return await _saveImage(image);
      }
      return null;
    } catch (e) {
      print('Error capturing image from camera: $e');
      return null;
    }
  }

  /// Pick image from gallery
  Future<String?> pickFromGallery() async {
    try {
      final XFile? image = await _picker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 1024,
        maxHeight: 1024,
        imageQuality: 85,
      );

      if (image != null) {
        return await _saveImage(image);
      }
      return null;
    } catch (e) {
      print('Error picking image from gallery: $e');
      return null;
    }
  }

  /// Save image to persistent storage
  Future<String> _saveImage(XFile image) async {
    final appDir = await getApplicationDocumentsDirectory();
    final imagesDir = Directory(path.join(appDir.path, 'cattle_images'));
    
    // Create directory if it doesn't exist
    if (!await imagesDir.exists()) {
      await imagesDir.create(recursive: true);
    }

    // Generate unique filename
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final fileName = 'cattle_$timestamp${path.extension(image.path)}';
    final savedPath = path.join(imagesDir.path, fileName);

    // Copy image to app directory
    final File imageFile = File(image.path);
    await imageFile.copy(savedPath);

    return savedPath;
  }

  /// Delete image file
  Future<bool> deleteImage(String imagePath) async {
    try {
      final file = File(imagePath);
      if (await file.exists()) {
        await file.delete();
        return true;
      }
      return false;
    } catch (e) {
      print('Error deleting image: $e');
      return false;
    }
  }

  /// Check if image file exists
  Future<bool> imageExists(String imagePath) async {
    try {
      final file = File(imagePath);
      return await file.exists();
    } catch (e) {
      return false;
    }
  }
}
