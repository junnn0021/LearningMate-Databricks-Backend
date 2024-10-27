# LearningMate-Databricks-Backend
##### LearningMate-Databricks-Backend

<hr>

### 파이썬 프로젝트 환경 설정 가이드
##### 이 프로젝트는 pyenv와 pip freeze를 사용하여 파이썬 버전과 패키지를 관리합니다.
##### 이 가이드를 따라 환경을 설정하여 프로젝트에 참여하세요.<p>
<hr>

**1. pyenv 설치**
##### pyenv는 다양한 파이썬 버전을 관리하는 도구입니다. 아래 명령어를 통해 pyenv를 설치하세요.

```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```
		
##### 그 다음, ~/.bashrc 파일을 열어 아래 내용을 추가하세요.

```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```
##### 재시작 후, 아래 파이썬 버전을 설치하세요.

```
pyenv install 3.9.0
```
<hr>
		
**2. pip 패키지 관리**
##### 이 프로젝트에서는 pip freeze를 사용하여 패키지를 관리합니다. requirements.txt 파일을 통해 패키지를 설치하세요.
```
pip install -r requirements.txt
```
##### 이 명령어를 통해 requirements.txt 파일 내에 정의된 패키지를 같은 버전으로 설치하여 버전 차이로 인한 오류를 방지합니다.
##### 패키지가 추가되어 requirements.txt 파일을 업데이트하려면 아래 명령어를 실행하세요.

```
pip freeze > requirements.txt
```
		
##### 그 다음, requirements.txt 파일을 GitHub에 업로드하세요.
```
서버 실행명령어:
uvicorn app.main:app --reload

```