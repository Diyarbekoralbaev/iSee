import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Take Photo App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: TakePhotoScreen(),
    );
  }
}

class TakePhotoScreen extends StatefulWidget {
  @override
  _TakePhotoScreenState createState() => _TakePhotoScreenState();
}

class _TakePhotoScreenState extends State<TakePhotoScreen> {
  File? _imageFile;

  // Function to open the camera and capture a photo
  Future<void> _takePhoto() async {
    final ImagePicker _picker = ImagePicker();
    final XFile? image = await _picker.pickImage(source: ImageSource.camera);

    setState(() {
      if (image != null) {
        _imageFile = File(image.path);
      }
    });

    // Send the image to the API if it's not null
    if (_imageFile != null) {
      await _sendImageToAPI(_imageFile!);
    }
  }

  // Function to send image to the API
  Future<void> _sendImageToAPI(File imageFile) async {
    try {
      // Read the image file as bytes
      List<int> imageBytes = await imageFile.readAsBytes();

      // Send the request with image bytes as the body
      var response = await http.post(
        Uri.parse('http://127.0.0.1:4444/generate_image_description/'),
        body: imageBytes,
        headers: {
          'Content-Type':
              'application/octet-stream', // Specify content type as binary
        },
      );

      // Handle response
      if (response.statusCode == 200) {
        // Successful API call
        print('Image successfully sent to API.');
        print('API Response: ${response.body}');
      } else {
        // Error in API call
        print(
            'Failed to send image to API. Status code: ${response.statusCode}');
        print('Error response: ${response.body}');
      }
    } catch (e) {
      print('Error123123: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Take Photo'),
      ),
      body: Center(
        child: _imageFile == null
            ? Text('No image selected.')
            : Image.file(_imageFile!),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _takePhoto,
        tooltip: 'Take Photo',
        child: Icon(Icons.camera),
      ),
    );
  }
}
