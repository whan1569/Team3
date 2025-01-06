import React from 'react';
import './MyPage.css';

function MyPage() {
  return (
    <div className="mypage">
      <div className="mypage_header">
        <div className="profile_section">
          <div className="profile_icon"><img src="/images/LG_logo.png" alt="LG Logo" className="logo-image" /></div>
          <div className="profile_name">
            <span>수정 &gt;</span>
          </div>
        </div>
      </div>

      <div className="section">
        <h2 className="section_title">시청기록</h2>
        <div className="section_content">
          {/* 여기에 코드 추가! */}
          콘텐츠를 시청하면 여기에 보여집니다.
        </div>
      </div>

      <div className="section">
        <h2 className="section_title">구매 리스트</h2>
        <div className="section_content">
          {/* 여기에 코드 추가! */}
          새 콘텐츠를 구매하거나 대여할 수 있습니다.
          {/* <button className="action_button">최신 콘텐츠 둘러보기</button> */}
        </div>
      </div>

      <div className="section">
        <h2 className="section_title">찜한 콘텐츠</h2>
        <div className="section_content">
          {/* 여기에 코드 추가! */}
          찜한 콘텐츠가 여기에서 보여집니다.
        </div>
      </div>
    </div>
  );
}

export default MyPage;
