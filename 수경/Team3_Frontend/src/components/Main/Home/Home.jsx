import React from "react";
import Banner from "../Banner/Banner.jsx"; // Banner 컴포넌트 임포트
import TOP20 from "../Recommend/Watching/TOP20.jsx";
import RecommendContents from "../Recommend/Recommend/RecommendContents.jsx";
import "./Home.css"; // 스타일링을 위한 CSS 파일 임포트

const Home = () => {
  return (
    <div className="main-container">
      <Banner /> {/* 배너 영역 */}
      <TOP20 />
      <RecommendContents />
    </div>
  );
};

export default Home;
