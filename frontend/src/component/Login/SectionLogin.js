import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, Alert } from 'react-bootstrap';
//axios.defaults.withCredentials = true;index.js에 설정
function SectionLogin() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('/auth/login', {
                username,
                password
            });

            if (response.status === 200) {
                const { accessToken, refreshToken, accessTokenExpiresIn } = response.data;
                axios.defaults.headers.common["Authorization"] = `Bearer ${accessToken}`

                localStorage.setItem('accessToken', accessToken);
                localStorage.setItem('accessTokenExpiresIn', accessTokenExpiresIn);
                //setRefreshTokenCookie(refreshToken);
                localStorage.setItem('refreshToken', refreshToken);
                //console.log('로그인 성공');
                localStorage.setItem('login', "1");
                localStorage.setItem('username', username);
                document.location.href='/';
            }
        } catch (error) {
            if  (error.response.status === 401) {
                console.error('로그인 실패:', error.response.statusText);
                setError('로그인에 실패했습니다. 다시 시도해주세요.');
            }
            else {
                console.error('네트워크 오류:', error);
                setError('네트워크 오류가 발생했습니다.');
            }
            //  document.location.href = '/'
            // localStorage.setItem('login', "1");
            // localStorage.setItem('username', username);
        }
    };

    /*
    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        else {
            return null; // 해당하는 이름의 쿠키가 없는 경우 null 반환
        }
    };*/

    return (
        <Container className="d-flex justify-content-center align-items-center vh-70" style={{marginTop:"100px"}}>
            <div className="text-center w-50">
                <h1><img alt="" src="titlelog.png" width="40" height="40" className="d-inline-block align" />{' '}Finance</h1>
                <Form className={"login-form"} onSubmit={handleLogin}>
                    <Form.Group controlId="formId">
                        <Form.Label>아이디</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="아이디를 입력하세요"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </Form.Group>
                    <Form.Group controlId="formPassword">
                        <Form.Label>비밀번호</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder="비밀번호를 입력하세요"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </Form.Group>
                    {error && <Alert variant="danger">{error}</Alert>}
                    <Button variant="primary" type="submit" className="mt-3">
                        로그인
                    </Button>
                </Form>
            </div>
        </Container>
    );
}

export default SectionLogin;