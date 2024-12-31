import 'package:flutter/material.dart';

class PageSwiper extends StatefulWidget {
  const PageSwiper({super.key});

  @override
  PageSwiperState createState() => PageSwiperState();
}

class PageSwiperState extends State<PageSwiper> {
  final PageController _pageController =
      PageController(viewportFraction: 0.6); // 초기 페이지를 중간으로 설정
  double _startPositionX = 0.0; // 드래그 시작 위치
  double _deltaX = 0.0; // 드래그된 거리
  final int _pageCount = 5; // 총 페이지 수
  final int initialPage = 1000; // 초기 페이지 (무한 루프처럼 보이게 설정)

  int get realPage => _pageController.page!.round() % _pageCount;

  @override
  Widget build(BuildContext context) {
    return Listener(
      // 마우스 또는 터치 시작 감지
      onPointerDown: (PointerDownEvent event) {
        setState(() {
          _startPositionX = event.position.dx;
        });
      },
      // 마우스 또는 터치 드래그 감지
      onPointerMove: (PointerMoveEvent event) {
        setState(() {
          _deltaX = event.position.dx - _startPositionX;
        });
      },
      // 마우스 또는 터치 끝 감지
      onPointerUp: (PointerUpEvent event) {
        if (_deltaX.abs() > 50) {
          // 드래그 거리가 일정 이상일 때 페이지 이동
          if (_deltaX > 0) {
            // 오른쪽으로 드래그
            _pageController.previousPage(
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeInOut,
            );
          } else {
            // 왼쪽으로 드래그
            _pageController.nextPage(
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeInOut,
            );
          }
        }
        // 초기화
        setState(() {
          _startPositionX = 0.0;
          _deltaX = 0.0;
        });
      },
      child: SizedBox(
        height: MediaQuery.of(context).size.height * 0.3,
        child: PageView.builder(
          controller: _pageController,
          itemBuilder: (context, index) {
            final pageIndex = index % _pageCount; // 루프처럼 보이게 페이지 계산
            return Container(
              margin: const EdgeInsets.symmetric(horizontal: 10),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(15),
                image: DecorationImage(
                  image: AssetImage('assets/images/img${pageIndex + 1}.jpg'),
                  fit: BoxFit.cover,
                ),
              ),
              child: Center(
                child: Text(
                  'Page ${pageIndex + 1}',
                  style: const TextStyle(
                    fontSize: 24,
                    color: Colors.white,
                    shadows: [
                      Shadow(
                        blurRadius: 10.0,
                        color: Colors.black,
                        offset: Offset(0, 2),
                      ),
                    ],
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
