import 'package:flutter/material.dart';
import 'section_title.dart';
import '../widgets/image_slider.dart';
import '../widgets/page_swiper.dart'; // PageSwiper 위젯 가져오기

class ResponsivePage extends StatelessWidget {
  const ResponsivePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('VOD Recommendation'), // 앱 제목 설정
        actions: [
          IconButton(
            icon: const Icon(Icons.search), // 검색 아이콘
            onPressed: () {
              debugPrint('Search button clicked');
            },
          ),
          IconButton(
            icon: const Icon(Icons.person), // 마이페이지 아이콘
            onPressed: () {
              debugPrint('Profile button clicked');
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 🖼️ 상단 이미지 스와이퍼 추가
              SizedBox(
                height: MediaQuery.of(context).size.height * 0.3,
                child: const PageSwiper(), // PageSwiper 추가
              ),
              const SizedBox(height: 24), // 간격 추가

              // 🏷️ 섹션 타이틀 및 이미지 슬라이더
              const SectionTitle(title: '#Festival'),
              const ImageSlider(keyword: 'festival'),
              const SizedBox(height: 16),

              const SectionTitle(title: '#Night'),
              const ImageSlider(keyword: 'night'),
              const SizedBox(height: 16),

              const SectionTitle(title: '#Winter'),
              const ImageSlider(keyword: 'winter'),
            ],
          ),
        ),
      ),
    );
  }
}
