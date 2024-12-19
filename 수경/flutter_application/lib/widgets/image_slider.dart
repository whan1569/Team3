import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_application/screen/image_detail_page.dart';
import 'package:flutter_application/gen/assets.gen.dart';

class ImageSlider extends StatelessWidget {
  final String keyword; // 검색할 키워드

  const ImageSlider({super.key, required this.keyword});

  // 키워드에 따라 이미지 필터링
  List<AssetGenImage> _getImages() {
    return Assets.images.values
        .where(
            (asset) => asset.path.toLowerCase().contains(keyword.toLowerCase()))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final images = _getImages();

    if (images.isEmpty) {
      return const Center(child: Text('No images found'));
    }

    return SizedBox(
      height: 180,
      child: ScrollConfiguration(
        behavior: const ScrollBehavior().copyWith(
          dragDevices: {
            PointerDeviceKind.touch,
            PointerDeviceKind.mouse, // 마우스 드래그 활성화
          },
        ),
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: images.length,
          itemBuilder: (context, index) {
            return GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) =>
                        ImageDetailPage(imageUrl: images[index].path),
                  ),
                );
              },
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 8.0),
                width: 250, // 이미지 너비 설정
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(12.0),
                  child: images[index].image(
                    fit: BoxFit.cover,
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
