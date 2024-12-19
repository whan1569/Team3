/// GENERATED CODE - DO NOT MODIFY BY HAND
/// *****************************************************
///  FlutterGen
/// *****************************************************

// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: directives_ordering,unnecessary_import,implicit_dynamic_list_literal,deprecated_member_use

import 'package:flutter/widgets.dart';

class $AssetsImagesGen {
  const $AssetsImagesGen();

  /// File path: assets/images/festival_01.jpg
  AssetGenImage get festival01 =>
      const AssetGenImage('assets/images/festival_01.jpg');

  /// File path: assets/images/festival_02.jpg
  AssetGenImage get festival02 =>
      const AssetGenImage('assets/images/festival_02.jpg');

  /// File path: assets/images/festival_03.jpg
  AssetGenImage get festival03 =>
      const AssetGenImage('assets/images/festival_03.jpg');

  /// File path: assets/images/festival_04.jpg
  AssetGenImage get festival04 =>
      const AssetGenImage('assets/images/festival_04.jpg');

  /// File path: assets/images/festival_05.jpg
  AssetGenImage get festival05 =>
      const AssetGenImage('assets/images/festival_05.jpg');

  /// File path: assets/images/m.png
  AssetGenImage get m => const AssetGenImage('assets/images/m.png');

  /// File path: assets/images/night_01.jpg
  AssetGenImage get night01 =>
      const AssetGenImage('assets/images/night_01.jpg');

  /// File path: assets/images/night_02.jpg
  AssetGenImage get night02 =>
      const AssetGenImage('assets/images/night_02.jpg');

  /// File path: assets/images/night_03.jpg
  AssetGenImage get night03 =>
      const AssetGenImage('assets/images/night_03.jpg');

  /// File path: assets/images/night_04.jpg
  AssetGenImage get night04 =>
      const AssetGenImage('assets/images/night_04.jpg');

  /// File path: assets/images/night_05.jpg
  AssetGenImage get night05 =>
      const AssetGenImage('assets/images/night_05.jpg');

  /// File path: assets/images/night_festival_01.jpg
  AssetGenImage get nightFestival01 =>
      const AssetGenImage('assets/images/night_festival_01.jpg');

  /// File path: assets/images/search.png
  AssetGenImage get search => const AssetGenImage('assets/images/search.png');

  /// List of all assets
  List<AssetGenImage> get values => [
        festival01,
        festival02,
        festival03,
        festival04,
        festival05,
        m,
        night01,
        night02,
        night03,
        night04,
        night05,
        nightFestival01,
        search
      ];
}

class Assets {
  Assets._();

  static const $AssetsImagesGen images = $AssetsImagesGen();
}

class AssetGenImage {
  const AssetGenImage(
    this._assetName, {
    this.size,
    this.flavors = const {},
  });

  final String _assetName;

  final Size? size;
  final Set<String> flavors;

  Image image({
    Key? key,
    AssetBundle? bundle,
    ImageFrameBuilder? frameBuilder,
    ImageErrorWidgetBuilder? errorBuilder,
    String? semanticLabel,
    bool excludeFromSemantics = false,
    double? scale,
    double? width,
    double? height,
    Color? color,
    Animation<double>? opacity,
    BlendMode? colorBlendMode,
    BoxFit? fit,
    AlignmentGeometry alignment = Alignment.center,
    ImageRepeat repeat = ImageRepeat.noRepeat,
    Rect? centerSlice,
    bool matchTextDirection = false,
    bool gaplessPlayback = true,
    bool isAntiAlias = false,
    String? package,
    FilterQuality filterQuality = FilterQuality.low,
    int? cacheWidth,
    int? cacheHeight,
  }) {
    return Image.asset(
      _assetName,
      key: key,
      bundle: bundle,
      frameBuilder: frameBuilder,
      errorBuilder: errorBuilder,
      semanticLabel: semanticLabel,
      excludeFromSemantics: excludeFromSemantics,
      scale: scale,
      width: width,
      height: height,
      color: color,
      opacity: opacity,
      colorBlendMode: colorBlendMode,
      fit: fit,
      alignment: alignment,
      repeat: repeat,
      centerSlice: centerSlice,
      matchTextDirection: matchTextDirection,
      gaplessPlayback: gaplessPlayback,
      isAntiAlias: isAntiAlias,
      package: package,
      filterQuality: filterQuality,
      cacheWidth: cacheWidth,
      cacheHeight: cacheHeight,
    );
  }

  ImageProvider provider({
    AssetBundle? bundle,
    String? package,
  }) {
    return AssetImage(
      _assetName,
      bundle: bundle,
      package: package,
    );
  }

  String get path => _assetName;

  String get keyName => _assetName;
}
