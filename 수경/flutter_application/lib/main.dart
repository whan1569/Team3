// main.dart
// 애플리케이션의 진입점 파일입니다. 여기에서 MyApp 클래스가 정의되고 실행됩니다.
import 'package:flutter/material.dart';
import 'screen/responsive_page.dart';

void main() {
  runApp(const MyApp()); // 앱을 실행시키는 메인 함수
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // MaterialApp을 정의하여 전체 앱의 테마와 시작 페이지를 설정합니다.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false, // 디버그 배너를 숨깁니다.
      theme: ThemeData(primarySwatch: Colors.blue), // 앱의 기본 테마 색상 설정
      home: const ResponsivePage(), // 앱의 홈 화면으로 ResponsivePage 설정
    );
  }
}
