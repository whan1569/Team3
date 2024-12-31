import 'package:flutter/material.dart';

// 클릭된 이미지의 세부 페이지 정의
class ImageDetailPage extends StatelessWidget {
  final String imageUrl; // 표시할 이미지 경로

  const ImageDetailPage({super.key, required this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Image Details'), // 페이지 제목
      ),
      body: Center(
        child: Image.asset(imageUrl), // assets에 있는 이미지를 표시
      ),
    );
  }
}
