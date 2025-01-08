import { ERROR_URL } from "../GlobalFeatures";
import { MessageBox, Wrapper } from "./Styled/Unknowns/UnknownStyled";

function Unknown() {
    return (
        <Wrapper img={ERROR_URL}>
            <MessageBox>
                <p>Oops! This page is currently not support yet!</p>
                <p>앗! 현재 이 페이지는 아직 지원하지 않습니다!</p>
                <p>sorry</p>
            </MessageBox>
        </Wrapper>
    );
}

export default Unknown;
