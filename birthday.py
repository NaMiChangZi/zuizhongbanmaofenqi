import streamlit as st
from streamlit.components.v1 import html
import base64

# 设置页面
st.set_page_config(page_title="🎂 生日惊喜", layout="wide")

# ---- 读取图片并转为 Base64 ----
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 你的图片文件名（请确保与下面一致）
img_base64 = get_image_base64("birthday_cat.png")

# ---- 侧边栏控制灯光 ----
st.sidebar.title("🎬 舞台控制")
if "light_on" not in st.session_state:
    st.session_state.light_on = False

if st.sidebar.button("💡 点亮舞台" if not st.session_state.light_on else "🌙 熄灭舞台"):
    st.session_state.light_on = not st.session_state.light_on
    st.rerun()

status = "✨ 已点亮" if st.session_state.light_on else "🌑 未点亮"
st.sidebar.markdown(f"**状态：{status}**")

# ---- 构建 HTML（包含所有舞台效果） ----
# 根据灯光状态添加不同的 CSS class
light_class = "light-on" if st.session_state.light_on else ""

# 嵌入 HTML
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}
  body {{
    overflow: hidden;
  }}
  .stage {{
    position: relative;
    width: 100%;
    height: 650px;
    background: radial-gradient(ellipse at center bottom, #1a0a2e 0%, #0d0a1a 80%);
    overflow: hidden;
    transition: background 1.2s ease;
    font-family: 'Comic Sans MS', cursive, sans-serif;
  }}
  /* 点亮后的背景 */
  .stage.light-on {{
    background: radial-gradient(ellipse at center bottom, #2a1a4e 0%, #0f0a20 80%);
  }}

  /* ------ 聚光灯（默认关闭） ------ */
  .spotlight {{
    position: absolute;
    top: -30%;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 120%;
    background: radial-gradient(ellipse at center top, rgba(255, 220, 180, 0) 0%, rgba(255, 200, 150, 0) 70%);
    pointer-events: none;
    transition: all 1.5s ease;
    opacity: 0;
    z-index: 2;
  }}
  .stage.light-on .spotlight {{
    opacity: 0.5;
    background: radial-gradient(ellipse at center top, rgba(255, 220, 180, 0.25) 0%, rgba(255, 180, 120, 0.08) 60%, transparent 80%);
  }}
  /* 第二层彩色光晕 */
  .spotlight-color {{
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    height: 110%;
    background: radial-gradient(ellipse at center top, rgba(255, 100, 200, 0) 0%, rgba(100, 150, 255, 0) 70%);
    pointer-events: none;
    transition: all 1.8s ease;
    opacity: 0;
    z-index: 1;
  }}
  .stage.light-on .spotlight-color {{
    opacity: 0.3;
    background: radial-gradient(ellipse at center top, rgba(255, 100, 200, 0.15) 0%, rgba(100, 150, 255, 0.1) 50%, transparent 80%);
  }}

  /* ------ 星星（始终存在） ------ */
  .stars {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
  }}
  .star {{
    position: absolute;
    background: white;
    border-radius: 50%;
    animation: twinkle 2s ease-in-out infinite alternate;
  }}
  @keyframes twinkle {{
    0% {{ opacity: 0.2; transform: scale(0.8); }}
    100% {{ opacity: 1; transform: scale(1.2); }}
  }}

  /* ------ 猫咪（舞台中央，呼吸浮动） ------ */
  .cat-wrapper {{
    position: absolute;
    bottom: 25%;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    cursor: pointer;
    animation: floatAndBreathe 3s ease-in-out infinite;
  }}
  .cat-wrapper img {{
    width: 220px;
    height: auto;
    display: block;
    filter: drop-shadow(0 0 20px rgba(255, 200, 150, 0.1));
    transition: filter 0.6s;
  }}
  .stage.light-on .cat-wrapper img {{
    filter: drop-shadow(0 0 30px rgba(255, 220, 180, 0.4));
  }}
  @keyframes floatAndBreathe {{
    0% {{ transform: translateX(-50%) translateY(0px) scale(1); }}
    50% {{ transform: translateX(-50%) translateY(-15px) scale(1.04); }}
    100% {{ transform: translateX(-50%) translateY(0px) scale(1); }}
  }}

  /* ------ 提示文字（底部居中，半透明） ------ */
  .hint {{
    position: absolute;
    bottom: 8%;
    left: 50%;
    transform: translateX(-50%);
    color: rgba(255, 255, 255, 0.5);
    font-size: 16px;
    background: rgba(0, 0, 0, 0.3);
    padding: 6px 18px;
    border-radius: 30px;
    backdrop-filter: blur(3px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 20;
    white-space: nowrap;
    letter-spacing: 1px;
    transition: opacity 0.5s;
  }}
  .stage.light-on .hint {{
    color: rgba(255, 255, 255, 0.7);
    background: rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 200, 150, 0.2);
  }}

  /* ------ Emoji 降落（雨） ------ */
  .emoji-rain {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 3;
  }}
  .emoji {{
    position: absolute;
    font-size: 2rem;
    animation: fall linear infinite;
    opacity: 0.6;
  }}
  @keyframes fall {{
    0% {{ transform: translateY(-10vh) rotate(0deg) scale(0.8); opacity: 0.3; }}
    100% {{ transform: translateY(110vh) rotate(720deg) scale(1.2); opacity: 0; }}
  }}

  /* 舞台边缘装饰线（点亮后显现） */
  .stage-edge {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, transparent, rgba(255, 200, 150, 0) 0%, transparent);
    transition: all 1.5s;
    z-index: 5;
  }}
  .stage.light-on .stage-edge {{
    background: linear-gradient(90deg, transparent, rgba(255, 200, 150, 0.4) 20%, rgba(255, 100, 200, 0.4) 50%, rgba(100, 150, 255, 0.4) 80%, transparent);
    box-shadow: 0 -5px 30px rgba(255, 200, 150, 0.1);
  }}
</style>
</head>
<body>
<div class="stage {light_class}">
    <!-- 星星背景 -->
    <div class="stars" id="stars-container"></div>

    <!-- 聚光灯层 -->
    <div class="spotlight"></div>
    <div class="spotlight-color"></div>

    <!-- 舞台边缘 -->
    <div class="stage-edge"></div>

    <!-- Emoji 雨 -->
    <div class="emoji-rain" id="emoji-rain"></div>

    <!-- 猫咪 -->
    <div class="cat-wrapper" id="cat-wrapper">
        <img src="data:image/png;base64,{img_base64}" alt="生日猫" id="cat-img">
    </div>

    <!-- 提示文字 -->
    <div class="hint" id="hint-text">🎵 点击小猫开始献唱</div>

    <!-- 音频（隐藏） -->
    <audio id="audio-player" src="your_reality" preload="auto" loop></audio>
</div>

<script>
    // ---- 生成星星 ----
    (function() {{
        const container = document.getElementById('stars-container');
        for (let i=0; i<60; i++) {{
            let star = document.createElement('div');
            star.className = 'star';
            let size = Math.random() * 3 + 1;
            star.style.width = size + 'px';
            star.style.height = size + 'px';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = (Math.random() * 5) + 's';
            star.style.animationDuration = (Math.random() * 3 + 2) + 's';
            container.appendChild(star);
        }}
    }})();

    // ---- 生成降落 Emoji ----
    (function() {{
        const container = document.getElementById('emoji-rain');
        const emojis = ['🎂', '🎉', '🎁', '🍰', '✨', '🥳', '🧁', '🎊', '💖', '🌸'];
        for (let i=0; i<30; i++) {{
            let span = document.createElement('span');
            span.className = 'emoji';
            span.textContent = emojis[Math.floor(Math.random() * emojis.length)];
            span.style.left = Math.random() * 100 + '%';
            span.style.fontSize = (Math.random() * 1.5 + 1.5) + 'rem';
            span.style.animationDuration = (Math.random() * 4 + 5) + 's';
            span.style.animationDelay = (Math.random() * 8) + 's';
            container.appendChild(span);
        }}
    }})();

    // ---- 音乐控制 ----
    const audio = document.getElementById('audio-player');
    const cat = document.getElementById('cat-wrapper');
    const hint = document.getElementById('hint-text');

    cat.addEventListener('click', function() {{
        if (audio.paused) {{
            audio.play().catch(e => console.log('播放失败'));
            hint.textContent = '🎵 正在献唱... 点击暂停';
        }} else {{
            audio.pause();
            hint.textContent = '🎵 点击小猫开始献唱';
        }}
    }});

    // 播放结束时自动循环（已设置 loop）
    // 更新提示（当播放结束时）
    audio.addEventListener('ended', function() {{
        // loop 会自动重新播放，但提示可以保持
        hint.textContent = '🎵 点击小猫开始献唱';
    }});
</script>
</body>
</html>
"""

# 显示 HTML
html(html_code, height=650)
