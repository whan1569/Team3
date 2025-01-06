import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // React Router 추가
import Header from './components/Header/Header.jsx';
import Home from './components/Main/Home.jsx';
import MyPage from "./components/MyPage/MyPage.jsx"; // MyPage 컴포넌트 임포트
import Search from "./components/Search/Search.jsx"; // Search 컴포넌트 임포트
import './App.css';

function App() {
  return (
    <Router>
      <Header />
      <div className='main'>
        <Routes>
          <Route path="/" element={<Home />} /> {/* 기본 홈 페이지 */}
          <Route path="/search" element={<Search />} /> {/* 검색 페이지 */}
          <Route path="/mypage" element={<MyPage />} /> {/* 마이페이지 */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;

