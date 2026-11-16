import os
import re
import urllib.request

# The 22 project items extracted directly from download.htm
projects_data = [
    {
        "id": "biedermeier",
        "title": "BIEDERMEIER LIFESTYLES \u2013 HUNGARIAN NATIONAL GALLERY",
        "desc": "",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/07be574f-c1e4-4e36-b514-ea2afa8d0393_carw_202x158x1920.jpg?h=942805494d9ae877d48c4ac2befd8cfb",
        "link": "/biedermeier-lifestyles-hungarian-national-gallery"
    },
    {
        "id": "like-you-me",
        "title": "LIKE YOU & ME",
        "desc": "LIKE YOU & ME - Young Hungarian Photography\nMAI MAN\u00d3 H\u00c1Z\n2023\n\nFeaturing nearly a hundred milestone works by thirty young artists, Like You and Me is an exhibition that highlights themes and technical experiments from contemporary Hungarian photography, along with characteristics of the genre and various cases when the boundaries of the medium are crossed.\n\nCurator: Zita S\u00c1RV\u00c1RI\nGraphic Design: Adrienn CS\u00c1SZ\u00c1R I Nora KASZANYI",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/4c8044de-d7d6-4642-b650-65b5100839a3_carw_202x158x1920.png?h=b2aa48e7fa4dbe6213dfbe708a26769a",
        "link": "/like-you-me"
    },
    {
        "id": "mome-diploma-2022",
        "title": "MOME DIPLOMA 2022",
        "desc": "Visual Identity for MOME (Moholy-Nagy University of Art and Design, Budapest) Graduations show 2022",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/de80e9fa-abfc-4107-aa73-d128e162723a_carw_202x158x1920.jpg?h=ef9dc48742fa2a0bec5a0cc5aa6396a0",
        "link": "/mome-diploma-2022"
    },
    {
        "id": "flow",
        "title": "FLOW",
        "desc": "",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/f1927b35-73e0-44bd-96e2-e295ff03c29c_carw_202x158x1920.jpg?h=f2f5b6d0adfc3565616bd5294f4e8e97",
        "link": "/flow"
    },
    {
        "id": "budapest-design-week",
        "title": "BUDAPEST DESIGN WEEK",
        "desc": "B R A N D I N G",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/067d50a9-2e38-421c-b307-2c853a8aac3a_carw_202x158x1920.gif?h=4713518a89e78fe0a641e1777f30580b",
        "link": "/budapest-design-week"
    },
    {
        "id": "dhirty",
        "title": "DHIRTY",
        "desc": "",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/30fc2979-4a50-4780-8f67-572911f67483_carw_202x158x1920.jpg?h=1ea5c1e0c56fda36da21983a6488c107",
        "link": "/dhirty"
    },
    {
        "id": "mome-2122",
        "title": "MOME 21/22",
        "desc": "",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/f85c9849-9854-432b-a7a8-7d7d0cfe4257_carw_202x158x1920.png?h=4fab7b2da154040dcfc958ede4092bd1",
        "link": "/mome-2122"
    },
    {
        "id": "superjuice",
        "title": "SUPERJUICE",
        "desc": "B R A N D I N G     /   P A C K A G I N G  ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/ccba2a18-eddb-44fd-8bb2-aed9f767b898_carw_202x158x1920.jpg?h=a05b413dee85f3ba857fba35c5ec083d",
        "link": "/superjuice"
    },
    {
        "id": "tactiles",
        "title": "tacTiles",
        "desc": " MA  Graduation project",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/5fe2ffef-6d66-44db-a491-3886d7c880aa_carw_202x158x1920.jpg?h=2afec8b81c40524efe6930240f1655bf",
        "link": "/tactiles-ma-graduation-project"
    },
    {
        "id": "armel-opera-festival",
        "title": "ARMEL OPERA FESTIVAL",
        "desc": "E D I T O R I A L",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/6002dec4-c8e9-4f83-960d-d44d7a01d691_carw_202x158x1920.jpg?h=cc63d83313152bc24ef6acb49502e505",
        "link": "/armel-opera-festival"
    },
    {
        "id": "knowledge-in-motion",
        "title": "KNOWLEDGE IN MOTION",
        "desc": "",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/2dd83b40-625d-42c3-8c5f-3b3a32afe377_carw_202x158x1920.jpg?h=a53804d2b5dd0b910160d72a6a49451c",
        "link": "/knowledge-in-motion"
    },
    {
        "id": "gaia-display",
        "title": "Gaia Display",
        "desc": "F O N T ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/4a3b80d8-e5a2-4c05-b21b-258c5aa64245_carw_202x158x1920.jpg?h=4e1a7de7f0c5b5e2827599777468ac68",
        "link": "/gaia-display"
    },
    {
        "id": "logos",
        "title": "LOGOS AND MARKS",
        "desc": "L O G O ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/0f65e0ba-6609-4d76-9ff9-e9ff2ea52794_rwc_173x0x3172x2480x1920.jpg?h=3c0961ebd7fb693911e70a21e0348768",
        "link": "/logos"
    },
    {
        "id": "mikrokosmos",
        "title": "MIKROKOSMOS",
        "desc": "E X P E R I M E N T A L / E D I T O R I A L ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/03a3f915-65ea-4f1f-8539-a0b8512f6775_carw_202x158x1920.jpg?h=1f39263bcb0346b402ce22699b639e8c",
        "link": "/mikrokosmos"
    },
    {
        "id": "zita-zsarnoczay",
        "title": "ZITA ZSARNOCZAY",
        "desc": "E D I T O R I A L ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/d4e7b373-34d8-404b-8b2d-42630e271eb5_carw_202x158x1920.jpg?h=8fafd990f11d2c6235e65304259b9ed7",
        "link": "/z-i-t-a-z-s-a-r-n-o-c-z-a-y"
    },
    {
        "id": "dose",
        "title": "DOSE",
        "desc": "B R A N D I G / P A C K A G I N G",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/127f5393-6bcf-4749-8821-880e8386cd8b_rwc_307x130x1301x1017x1920.jpg?h=0dfc1e8e8f4c17809f9420bcab2b1912",
        "link": "/dose"
    },
    {
        "id": "moov",
        "title": "MOOV",
        "desc": "D A T A V I S U A L I S A T I O N ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/6341583b-c849-41b4-bcb4-bf86b4d7f32e_carw_202x158x1920.jpg?h=cb7919c890ad110b46837ad991d546f1",
        "link": "/moov"
    },
    {
        "id": "design-culture",
        "title": "DESIGN CULTURE AND SOMAESTHETICS CONFERENCE BUDAPEST",
        "desc": "C O N F E R E N C E \n",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/42cb26ef-6093-46a0-89c7-ac7a20a1d296_carw_202x158x1920.gif?h=d1202696d7d989501683631a442a9a26",
        "link": "/design-culture-and-somaesthetics-conference-budapest"
    },
    {
        "id": "thesis",
        "title": "THESIS",
        "desc": "E D I T O R I A L\n\n",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/be5f25da-30d8-4403-9507-8d4dfdc40179_carw_202x158x1920.jpg?h=4ab59575d74f6029d7dd5fb703eac994",
        "link": "/thesis"
    },
    {
        "id": "moholy",
        "title": "MOHOLY",
        "desc": "E X P E R I M E N T A L / T Y P O ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/f16400f5-b7da-4dc1-8e8f-aa286e175316_rwc_0x104x1920x1501x1920.png?h=e26800ebe37c780b242888fa9a3d6bda",
        "link": "/typographic-experiments"
    },
    {
        "id": "chair-transformation",
        "title": "CHAIR TRANSFORMATION",
        "desc": "E X H I B I T I O N   D E S I G N ",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/17d52c21-541c-4d1e-b509-14fe4efca1cc_carw_202x158x1920.jpg?h=4aad66430bc71bf5e8cd1d6c1b62160d",
        "link": "/chair-transformation"
    },
    {
        "id": "florian",
        "title": "FLORIAN",
        "desc": "B R A N D I N G / P A C K A G I N G",
        "img_url": "https://cdn.myportfolio.com/793e6874-b9e2-46f3-b2fd-d09cce63cfc3/38a49927-5a7e-4a24-a4c3-c9dce5a19e92_rwc_282x0x3274x2560x1920.jpg?h=9bee4006e4c9a84c07472861fb51a361",
        "link": "/f-l-o-r-i-a-n"
    }
]

out_dir = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\static\images\projects"
os.makedirs(out_dir, exist_ok=True)

for p in projects_data:
    ext = ".jpg"
    if ".png" in p["img_url"]:
        ext = ".png"
    elif ".gif" in p["img_url"]:
        ext = ".gif"
    fname = f"{p['id']}{ext}"
    fpath = os.path.join(out_dir, fname)
    p["local_img"] = f"/static/images/projects/{fname}"
    if not os.path.exists(fpath):
        try:
            req = urllib.request.Request(p["img_url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                data = resp.read()
            with open(fpath, "wb") as f:
                f.write(data)
            print(f"Downloaded {fname} ({len(data)} bytes)")
        except Exception as e:
            print(f"Error {fname}: {e}")
    else:
        print(f"Already have {fname}")

import json
data_file = r"C:\Users\NITHIN RAGUNATH\.gemini\antigravity\scratch\portfolio\projects_data.json"
with open(data_file, "w", encoding="utf-8") as f:
    json.dump(projects_data, f, indent=2)

print("Finished saving projects_data.json and downloading project images!")
