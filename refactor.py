import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

main_match = re.search(r'(<!-- Main Content Canvas -->.*?<main.*?>)(.*?)(</main>)', html, re.DOTALL)
main_pre, main_content, main_post = main_match.groups()

def ext(tag):
    pattern = rf'(<!-- {tag} -->.*?</section>)'
    res = re.search(pattern, main_content, re.DOTALL)
    # the finish workout section has no trailing \n, so regex might struggle. 
    # lets use a more forgiving regex
    if not res:
        pattern = rf'(<!-- {tag} -->.*?</section>)'
        res = re.search(pattern, main_content, re.DOTALL | re.IGNORECASE)
    return res.group(1) if res else ''

hero = ext('Hero Brand Typography Section')
active = ext('Active Workout Section')
activity = ext('Activity Log Section')
grid = ext('Dynamic Empty Content Grid')
map_sec = ext('Map Section')
camera = ext('Camera Section')
coach = ext('AI Coach Section')
finish = ext('Finish Workout Section')

# The Leaflet map size fix
map_sec = map_sec.replace('const map = L.map', 'window.leafletMap = L.map')

new_main_content = f"""
        <!-- TAB: HOME -->
        <div id="tab-home" class="tab-content block pb-20 w-full animate-[slideUpFade_0.4s_ease-out]">
{hero}
{active}
{activity}
{grid}
{finish}
        </div>

        <!-- TAB: PLAN -->
        <div id="tab-plan" class="tab-content hidden pb-20 w-full">
            <div class="mb-6">
                <h2 class="font-headline text-3xl font-black italic tracking-tighter uppercase text-secondary">Açık Hava Planı</h2>
                <p class="text-on-surface-variant text-sm mt-1 font-medium">Nefes al ve dışarıda koş.</p>
            </div>
{map_sec}
        </div>

        <!-- TAB: COACH -->
        <div id="tab-coach" class="tab-content hidden pb-20 w-full">
            <div class="mb-6">
                <h2 class="font-headline text-3xl font-black italic tracking-tighter uppercase text-[#f09dff]">Yapay Zeka</h2>
                <p class="text-on-surface-variant text-sm mt-1 font-medium">Akıllı antrenörün emrinde.</p>
            </div>
{coach}
        </div>

        <!-- TAB: USER -->
        <div id="tab-user" class="tab-content hidden pb-20 w-full">
            <div class="mb-6">
                <h2 class="font-headline text-3xl font-black italic tracking-tighter uppercase text-primary">Profil</h2>
                <p class="text-on-surface-variant text-sm mt-1 font-medium">Antrenman hatıralarını sakla.</p>
            </div>
{camera}
        </div>
"""

new_main = main_pre + new_main_content + main_post

nav_match = re.search(r'(<!-- Floating Bottom Navigation -->.*?</div>)', html, re.DOTALL)
old_nav = nav_match.group(1) if nav_match else ''

new_nav = '''<!-- Floating Bottom Navigation -->
    <div class="fixed bottom-6 left-0 w-full px-5 pointer-events-none z-50">
        <nav class="pointer-events-auto flex justify-around items-center px-1.5 py-3 bg-surface-container-highest/85 backdrop-blur-2xl rounded-[32px] border border-white/5 shadow-[0_16px_40px_rgba(0,0,0,0.6)]">
            <!-- Dashboard (Active) -->
            <a onclick="switchTab('tab-home', this)" class="nav-item nav-active flex flex-col items-center justify-center text-primary bg-primary/10 rounded-[22px] px-4 py-2 transition-all duration-300 cursor-pointer">
                <span class="material-symbols-outlined text-[24px]" style="font-variation-settings: 'FILL' 1;">grid_view</span>
                <span class="font-headline text-[9px] font-black tracking-widest uppercase mt-1">HOME</span>
            </a>
            <!-- Plan -->
            <a onclick="switchTab('tab-plan', this)" class="nav-item flex flex-col items-center justify-center text-on-surface-variant hover:text-secondary hover:bg-secondary/10 rounded-[22px] px-4 py-2 transition-all duration-300 cursor-pointer">
                <span class="material-symbols-outlined text-[24px]">map</span>
                <span class="font-headline text-[9px] font-bold tracking-widest uppercase mt-1">PLAN</span>
            </a>
            <!-- AI Coach -->
            <a onclick="switchTab('tab-coach', this)" class="nav-item flex flex-col items-center justify-center text-on-surface-variant hover:text-[#f09dff] hover:bg-[#f09dff]/10 rounded-[22px] px-4 py-2 transition-all duration-300 cursor-pointer">
                <span class="material-symbols-outlined text-[24px]">smart_toy</span>
                <span class="font-headline text-[9px] font-bold tracking-widest uppercase mt-1">COACH</span>
            </a>
            <!-- User -->
            <a onclick="switchTab('tab-user', this)" class="nav-item flex flex-col items-center justify-center text-on-surface-variant hover:text-primary hover:bg-primary/10 rounded-[22px] px-4 py-2 transition-all duration-300 cursor-pointer">
                <span class="material-symbols-outlined text-[24px]">person</span>
                <span class="font-headline text-[9px] font-bold tracking-widest uppercase mt-1">USER</span>
            </a>
        </nav>
    </div>'''

if old_nav:
    html = html.replace(old_nav, new_nav)
html = html.replace(main_match.group(0), new_main)

script = """
    <script>
        function switchTab(tabId, element) {
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.add('hidden');
                el.classList.remove('block');
            });
            const target = document.getElementById(tabId);
            if (target) {
                target.classList.remove('hidden');
                target.classList.add('block');
                
                target.style.animation = 'none';
                void target.offsetWidth; 
                target.style.animation = 'slideUpFade 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) both'; 
            }

            document.querySelectorAll('.nav-item').forEach(el => {
                el.className = el.className.replace(/nav-active|text-primary|bg-primary\\/10|text-secondary|bg-secondary\\/10|text-\\[#f09dff\\]|bg-\\[#f09dff\\]\\/10/g, '').trim();
                el.classList.add('text-on-surface-variant');
            });
            
            // Re-apply appropriate colors based on the tab
            if (element) {
                element.classList.remove('text-on-surface-variant');
                element.classList.add('nav-active');
                if (tabId === 'tab-home') element.classList.add('text-primary', 'bg-primary/10');
                if (tabId === 'tab-plan') element.classList.add('text-secondary', 'bg-secondary/10');
                if (tabId === 'tab-coach') element.classList.add('text-[#f09dff]', 'bg-[#f09dff]/10');
                if (tabId === 'tab-user') element.classList.add('text-primary', 'bg-primary/10');
            }
            
            if (tabId === 'tab-plan' && window.leafletMap) {
                setTimeout(() => window.leafletMap.invalidateSize(), 100);
            }
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
    </script>
</body>"""

html = html.replace('</body>', script)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
