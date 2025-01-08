import { createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  @font-face {
    font-family: 'LGEHeadline';
    src: url('/fonts/LGEIHeadlineTTF-Bold.ttf') format('truetype');
    font-weight: bold;
    font-style: normal;
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'LGEHeadline', -apple-system, BlinkMacSystemFont, sans-serif;
  }

  /* 메뉴 관련 스타일 */
  .menu-item {
    &:hover {
      color: #ED174D;
    }
  }

  /* 선택된 메뉴 스타일 */
  .menu-item.active {
    color: #ED174D;
  }
`; 