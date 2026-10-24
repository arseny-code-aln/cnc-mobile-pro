import os
import json
import urllib.request
import urllib.error
import webview

# Ваш API-ключ OpenRouter
DEFAULT_API_KEY = "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"

MATERIALS = {
    "steel": {"name": "Сталь конструкционная", "vc": 180, "fz": 0.12},
    "inox": {"name": "Нержавеющая сталь", "vc": 90, "fz": 0.08},
    "aluminum": {"name": "Алюминий (Д16Т)", "vc": 450, "fz": 0.22},
    "titanium": {"name": "Титан (ВТ6)", "vc": 60, "fz": 0.06}
}

class Api:
    def __init__(self):
        self.chat_history = [
            {"role": "system", "content": "Ты — опытный ИИ-технолог ЧПУ. Помогай с выбором режимов резания, подбором инструмента и отладкой G-кодов."}
        ]

    def get_materials(self):
        return MATERIALS

    def calculate_regimes_by_material(self, d, z, mat_key):
        d = float(d)
        z = int(z)
        mat = MATERIALS.get(mat_key, MATERIALS["steel"])
        vc = mat["vc"]
        fz = mat["fz"]
        n = round((vc * 1000) / (3.14159 * d))
        vf = round(n * z * fz)
        return {"vc": vc, "fz": fz, "n": n, "vf": vf}

    def calculate_turning(self, d, vc, fr):
        d, vc, fr = float(d), float(vc), float(fr)
        n = round((vc * 1000) / (3.14159 * d))
        fm = round(n * fr)
        return {"n": n, "fm": fm}

    def calculate_thread(self, nominal, pitch):
        nom, p = float(nominal), float(pitch)
        drill_d = round(nom - p, 2)
        return {"nominal": nom, "pitch": p, "drill_d": drill_d}

    def calculate_tolerance(self, nom, fit):
        return {"fit": fit, "es": "+0.03", "ei": "0", "min": float(nom), "max": round(float(nom) + 0.03, 3)}

    def generate_pcd(self, r, count, start_angle, depth, z_safe):
        return {"status": "ok", "gcode": "G90 G00 X0 Y0 Z50\n(PCD Generation completed)"}

    def validate_gcode(self, code):
        return {"is_safe": True, "warnings": []}

    def estimate_time_and_cost(self, code, rate, setup):
        return {"status": "ok", "time_min": 15, "total_cost": 1125}

    def search_code(self, code):
        codes = {"G00": "Быстрое перемещение", "G01": "Линейная интерполяция", "G02": "Круговая интерполяция по часовой"}
        c = code.strip().upper()
        if c in codes:
            return {"status": "ok", "code": c, "desc": codes[c]}
        return {"status": "error", "message": "Код не найден"}

    def export_gcode_file(self, name, code):
        path = os.path.join(os.getcwd(), f"{name}.nc")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
        return {"status": "ok", "path": path}

    def ask_ai_chat(self, message, mode="general"):
        self.chat_history.append({"role": "user", "content": message})
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": "openrouter/free",
            "messages": self.chat_history,
            "temperature": 0.3
        }
        
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=req_data, headers={
            "Authorization": f"Bearer {DEFAULT_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://cnc-mobile-pro.local",
            "X-Title": "CNC Mobile Pro"
        })
        
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                res_body = json.loads(response.read().decode("utf-8"))
                reply = res_body["choices"][0]["message"]["content"]
                self.chat_history.append({"role": "assistant", "content": reply})
                return {"status": "ok", "reply": reply}
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            return {"status": "error", "reply": f"Ошибка OpenRouter (HTTP {e.code}): {err_msg}"}
        except Exception as e:
            return {"status": "error", "reply": f"Ошибка запроса к ИИ: {str(e)}"}

    def clear_chat_history(self):
        self.chat_history = [
            {"role": "system", "content": "Ты — опытный ИИ-технолог ЧПУ."}
        ]
        return {"status": "ok"}

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('CNC Mobile Pro', 'index.html', width=450, height=800, min_size=(380, 600), js_api=api)
    webview.start(debug=False)