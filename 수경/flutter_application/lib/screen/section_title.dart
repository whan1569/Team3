import 'package:flutter/material.dart';

// 섹션 제목 위젯 정의
class SectionTitle extends StatelessWidget {
  final String title; // 섹션의 제목 텍스트

  const SectionTitle({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0), // 위아래로 여백 설정
      child: Text(
        title, // 제목 텍스트 표시
        style: const TextStyle(
          fontSize: 20, // 텍스트 크기 설정
          fontWeight: FontWeight.bold, // 텍스트 굵기 설정
        ),
      ),
    );
  }
}
