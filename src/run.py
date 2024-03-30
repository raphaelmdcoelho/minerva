from app import create_app

print(f'Running the app... starting with the file: {__name__}')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)