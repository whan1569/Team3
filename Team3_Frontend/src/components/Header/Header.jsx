import React from "react";
import { FiSearch, FiUser } from "react-icons/fi";
import { useNavigate, useLocation } from "react-router-dom"; // useLocation 추가
import "./Header.css";
import WeatherWidget from "./WeatherWidget.jsx";

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation(); // 현재 경로 확인

  const handleSearchClick = () => {
    navigate("/search");
  };

  const handleMyPageClick = () => {
    navigate("/mypage");
  };

  const handleLogoClick = () => {
    navigate("/");
  };

  return (
    <header className="header">
      <div className="logo" onClick={handleLogoClick}>
        <img src="/images/LG_logo.png" alt="LG Logo" className="logo-image" />
        <span className="logo-text"><span className="Hello">Hello</span>TV</span>
      </div>
      <nav>
        <ul>
          <li>영화</li>
          <li>예능</li>
          <li>드라마</li>
          <li>키즈/애니</li>
        </ul>
      </nav>
      <div className="icons">
        {/* 검색 아이콘: 검색 페이지에서는 숨김 */}
        {location.pathname !== "/search" && (
          <FiSearch className="icon" onClick={handleSearchClick} />
        )}

        {/* 마이페이지 아이콘: 마이페이지일 때는 분홍색 */}
        <FiUser
          className={`icon ${location.pathname === "/mypage" ? "active" : ""}`}
          onClick={handleMyPageClick}
        />

        {/* 날씨 위젯 */}
        <WeatherWidget />
      </div>
    </header>
  );
};

export default Header;
