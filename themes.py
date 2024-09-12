def apply_theme(root, theme_name="light"):
    if theme_name == "dark":
        root.configure(bg="#282c34")
    elif theme_name == "light":
        root.configure(bg="#f0f4f5")
    elif theme_name == "colorful":
        root.configure(bg="#ffeb3b")
