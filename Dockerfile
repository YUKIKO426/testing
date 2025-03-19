EXPOSE 8000
CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "8000"]
