import os

def check_cycle():
    files = {
        'Rover': '',
        'Coordinates': ''
    }

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for root, _, filenames in os.walk(base_dir):
        for f in filenames:
            if f.endswith('.cs'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    for key in files:
                        if key in content:
                            files[key] += f + " "

    if all(files.values()):
        print("❌ Dépendance circulaire détectée entre Rover et Coordinates")
        exit(1)
    else:
        print("✅ Pas de dépendance circulaire")

if __name__ == "__main__":
    check_cycle()
