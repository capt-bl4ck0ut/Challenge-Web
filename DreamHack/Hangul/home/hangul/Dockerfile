FROM python:3.13@sha256:385ccb8304f6330738a6d9e6fa0bd7608e006da7e15bc52b33b0398e1ba4a15b

ENV user hangul

RUN apt update
RUN pip install flask

RUN useradd -d /home/$user $user

ADD app.py /home/$user/app.py
ADD flag /home/$user/flag

RUN chown -R root:root /home/$user
RUN chown root:$user /home/$user/app.py
RUN chown root:$user /home/$user/flag

RUN chmod 755 /home/$user/app.py
RUN chmod 755 /home/$user/flag

WORKDIR /home/$user
USER $user
EXPOSE 5000
CMD ["python", "app.py"]