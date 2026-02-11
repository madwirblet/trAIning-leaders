import os

def bundle():
    """Bundle HTML, CSS, and JavaScript into a single footer file for Thinkific."""
    try:
        with open('index.html', 'r') as f:
            html = f.read()
        with open('styles.css', 'r') as f:
            css = f.read()
        with open('script.js', 'r') as f:
            js = f.read()

        # Create properly formatted footer
        combined = f"""<style>
{css}
</style>
{html}
<script>
{js}
</script>"""
        
        with open('thinkific_footer.html', 'w') as f:
            f.write(combined)
        print("✓ Successfully bundled for Thinkific!")
        print(f"  Output file: thinkific_footer.html")
        print(f"  File size: {os.path.getsize('thinkific_footer.html')} bytes")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("  Make sure index.html, styles.css, and script.js exist in this directory.")
        exit(1)
    except Exception as e:
        print(f"✗ Error during bundling: {e}")
        exit(1)

if __name__ == "__main__":
    bundle()