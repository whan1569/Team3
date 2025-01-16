// src/Styled/Unknowns/UnknownStyled.tsx
import styled from 'styled-components';

export const Wrapper = styled.div<{ img: string }>`
    background-image: url(${props => props.img});
    background-size: cover;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
`;

export const MessageBox = styled.div`
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 20px;
    border-radius: 10px;
`;
