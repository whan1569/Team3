import React from "react";
import { LuGithub } from "react-icons/lu";    // git
import { FiHome } from "react-icons/fi";    // home
import { FaInstagram } from "react-icons/fa";   // instagram
import { RxNotionLogo } from "react-icons/rx";    // notion
import "./Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-logo">
        <img src="/images/LG_logo.png" alt="LG Logo" className="logo-image" />
        <h1>Hello <span>tv</span></h1>
      </div>
      <div className="footer-icons">
        <a href="https://github.com/whan1569/Team3" className="icon icon-git"><LuGithub /></a>
        <a href="https://www.lghellovision.net/main.do?utm_source=TPS_HP&utm_medium=TPS_HP&utm_campaign=TPS_HP&utm_content=lghv_totalMain" className="icon icon-home"><FiHome /></a>
        <a href="#" className="icon icon-instagram"><FaInstagram /></a>
        <a href="https://www.notion.so/Team-3-15ec68f616d48040ad18e7a76da4f646" className="icon icon-notion"><RxNotionLogo /></a>
      </div>
      <div className="footer-info">
        <p>대표이사 : 송구영 | 서울특별시 마포구 월드컵북로 56길 19 상암디지털드림타워</p>
        <p>사업자등록번호: 117-81-13423</p>
        <p>통신판매업 신고번호: 2017-서울마포-0254</p>
        <p>개인정보보호책임자 : 윤영식</p>
        <p>
          고객행복센터 : 1855-1000 | 070-7373-1002~3 (유료 / 월~금 전용) |
          080-120-1012 (무료 / 타사 전화 이용 시) 신규가입문의: 1855-1082
        </p>
      </div>
      <div className="footer-links">
        <a href="https://www.lghellovision.net/etcService/privateAdditionPromise.do">개인정보처리방침</a> |{" "}
        <a href="https://www.lghellovision.net/etcService/additionPromise.do">이용약관</a> |{" "}
        <a href="https://www.lghellovision.net/etcService/serviceAdditionPromise.do">서비스이용약관</a> |{" "}
        <a href="https://www.lghellovision.net/etcService/autoPayAdditionPromise.do">자동이체이용약관</a> |{" "}
        <a href="https://www.lghellovision.net/etcService/lawRuleAdditionPromise.do">법적고지</a> |{" "}
        <a href="https://ethics.lg.co.kr/index.do">정도경영 사이버신문고</a> |{" "}
        <a href="https://ch.lghellovision.net/support/advertising.do?soCode=SC00000000">광고문의</a> |{" "}
        <a href="https://www.lghellovision.net/customer/noPayBackService/noPayBack.do">미환급액 조회</a>
      </div>
      <div className="footer-links">
        <a href="https://www.msafer.or.kr/index.do">명의도용 방지 서비스(Msafer)</a> |{" "}
        <a href="https://www.lghellovision.net/customer/preventGuide/stageGuide.do">이용자 피해 예방 가이드</a> |{" "}
        <a href="https://corp.lghellovision.net/footer/customerService.do">고객서비스 현장</a> |{" "}
        <a href="https://spam.kisa.or.kr/spam/main.do">불법스팸대응센터</a> |{" "}
        <a href="https://www.msafer.or.kr/minwon_center/introduction.do">통신민원조정센터</a> |{" "}
        <a href="https://www.lghellovision.net/sitemap.do">사이트맵</a>
      </div>
      <p className="footer-copyright">
        &copy; 2024 Team3 X LG HelloVision All rights reserved.
      </p>
    </footer>
  );
};

export default Footer;
