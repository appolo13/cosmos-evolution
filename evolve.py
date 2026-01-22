#!/usr/bin/env python3
"""
COSMOS-9182 Evolution Engine
DNA 기반 자동 진화 시스템
"""

import json
import random
import os
from datetime import datetime
from typing import Dict, List, Any

# 설정
EPOCHS_PER_RUN = 100  # 실행당 진화할 epoch 수
ACCIDENT_CHANCE = 0.15  # 우연 발생 확률 (frequent 설정)

class EvolutionEngine:
    def __init__(self, world_state: Dict):
        self.world = world_state
        self.current_epoch = world_state["universe"]["current_epoch"]
        self.new_events = []
        self.new_accidents = []
        
    def evolve(self, epochs: int = EPOCHS_PER_RUN):
        """메인 진화 루프"""
        for _ in range(epochs):
            self.current_epoch += 1
            self._process_accidents()
            self._process_entities()
            self._check_contacts()
            self._check_discoveries()
            self._check_new_life()
        
        self._update_world_state()
        return self.world
    
    def _process_accidents(self):
        """우연 이벤트 발생"""
        if random.random() < ACCIDENT_CHANCE:
            accident = self._generate_accident()
            if accident:
                self.new_accidents.append(accident)
                self._apply_accident(accident)
    
    def _generate_accident(self) -> Dict:
        """우연 이벤트 생성"""
        accident_types = [
            {"type": "natural_disaster", "subtypes": ["earthquake", "flood", "drought", "storm", "volcanic"]},
            {"type": "resource_discovery", "subtypes": ["fertile_land", "metal_deposit", "water_source", "special_material"]},
            {"type": "mutation", "subtypes": ["genius_born", "prophet_born", "leader_born", "artist_born"]},
            {"type": "disease", "subtypes": ["plague", "mild_illness"]},
            {"type": "celestial", "subtypes": ["meteor_shower", "eclipse", "bright_star", "comet"]},
            {"type": "anomaly", "subtypes": ["time_distortion", "void_whisper", "memory_echo", "strange_dream"]},
        ]
        
        category = random.choice(accident_types)
        subtype = random.choice(category["subtypes"])
        
        # 영향받는 대상 선택
        affected = self._select_random_entity()
        if not affected:
            return None
            
        severity = random.uniform(0.3, 1.0)
        
        return {
            "epoch": self.current_epoch,
            "type": category["type"],
            "subtype": subtype,
            "affected": affected["id"],
            "severity": round(severity, 2),
            "resolved": False
        }
    
    def _apply_accident(self, accident: Dict):
        """우연 이벤트 적용"""
        entity = self._get_entity(accident["affected"])
        if not entity:
            return
            
        dna = entity.get("dna", {}).get("innate", {})
        expressed = entity.get("dna", {}).get("expressed", {})
        
        # DNA에 따른 반응 계산
        response = self._calculate_response(entity, accident)
        
        # 결과 적용
        if accident["type"] == "natural_disaster":
            # 적응력에 따른 피해
            adaptability = dna.get("adaptability", 5)
            damage = accident["severity"] * (10 - adaptability) / 10
            pop_loss = int(entity["population"] * damage * 0.1)
            entity["population"] = max(10, entity["population"] - pop_loss)
            
            # 높은 영성 = 종교적 해석
            if dna.get("spirituality", 5) > 6:
                self._add_cultural_element(entity, "myths", f"신의 시험 ({accident['subtype']})")
            
        elif accident["type"] == "resource_discovery":
            if accident["subtype"] == "special_material":
                if "discovered_resources" not in entity:
                    entity["discovered_resources"] = []
                entity["discovered_resources"].append({
                    "type": random.choice(["time_crystal_fragment", "memory_stone_piece", "void_touched_metal"]),
                    "epoch": self.current_epoch
                })
            # 호기심 높으면 연구, 영성 높으면 숭배
            if dna.get("curiosity", 5) > dna.get("spirituality", 5):
                self._add_cultural_element(entity, "values", "탐구정신")
            else:
                self._add_cultural_element(entity, "rituals", "발견물 숭배")
                
        elif accident["type"] == "mutation":
            # 특별한 개인 탄생 기록
            individual = {
                "type": accident["subtype"],
                "born": self.current_epoch,
                "influence": accident["severity"]
            }
            if "notable_individuals" not in entity:
                entity["notable_individuals"] = []
            entity["notable_individuals"].append(individual)
            
        elif accident["type"] == "celestial":
            # 우주 감수성에 따른 반응
            cosmic = dna.get("cosmic_sensitivity", 5)
            if cosmic > 6:
                self._add_cultural_element(entity, "myths", f"하늘의 징조 ({accident['subtype']})")
                # 높은 우주 감수성 + 천체 이벤트 = 천문학 관심 증가
                if "astronomy_interest" not in entity:
                    entity["astronomy_interest"] = 0
                entity["astronomy_interest"] += accident["severity"]
                
        elif accident["type"] == "anomaly":
            # 변칙 현상 - 세계의 특수 자원과 연결
            if dna.get("spirituality", 5) > 7:
                self._add_cultural_element(entity, "myths", f"신비로운 현상 ({accident['subtype']})")
            if dna.get("curiosity", 5) > 7:
                entity["anomaly_awareness"] = entity.get("anomaly_awareness", 0) + 1
        
        # 이벤트 기록
        self._record_event(accident, response, entity)
    
    def _calculate_response(self, entity: Dict, accident: Dict) -> str:
        """DNA 기반 반응 계산"""
        dna = entity.get("dna", {}).get("innate", {})
        
        responses = []
        
        # 공격성 체크
        if dna.get("aggression", 5) > 7:
            responses.append("공격적 대응")
        
        # 사회성 체크
        if dna.get("sociality", 5) > 7:
            responses.append("집단 협력")
        
        # 적응력 체크
        if dna.get("adaptability", 5) > 7:
            responses.append("빠른 적응")
        
        # 영성 체크
        if dna.get("spirituality", 5) > 7:
            responses.append("종교적 해석")
            
        # 호기심 체크
        if dna.get("curiosity", 5) > 7:
            responses.append("탐구적 접근")
        
        return ", ".join(responses) if responses else "소극적 대응"
    
    def _process_entities(self):
        """각 엔티티 처리"""
        for planet_id, entities in self.world.get("entities", {}).items():
            for entity in entities:
                self._grow_population(entity)
                self._evolve_culture(entity)
                self._check_stage_advancement(entity)
                self._apply_dna_drift(entity)
    
    def _grow_population(self, entity: Dict):
        """인구 성장"""
        base_growth = 0.001  # 0.1% 기본 성장
        dna = entity.get("dna", {}).get("innate", {})
        
        # 사회성이 높으면 성장률 증가
        sociality_bonus = (dna.get("sociality", 5) - 5) * 0.0002
        
        # 공격성이 높으면 내부 갈등으로 성장률 감소
        aggression_penalty = (dna.get("aggression", 5) - 5) * 0.0001
        
        growth_rate = base_growth + sociality_bonus - aggression_penalty
        growth = int(entity["population"] * growth_rate)
        
        entity["population"] = min(entity["population"] + max(0, growth), 10000000)  # 최대 인구 제한
    
    def _evolve_culture(self, entity: Dict):
        """문화 진화"""
        dna = entity.get("dna", {}).get("innate", {})
        
        # 가끔 새로운 문화 요소 발생
        if random.random() < 0.001:  # 0.1% 확률
            if dna.get("spirituality", 5) > 6:
                self._add_cultural_element(entity, "rituals", self._generate_ritual(dna))
            if dna.get("sociality", 5) > 6:
                self._add_cultural_element(entity, "values", self._generate_value(dna))
    
    def _generate_ritual(self, dna: Dict) -> str:
        """의식 생성"""
        rituals = [
            "계절 축제", "성인식", "조상 숭배", "수확 감사", 
            "별 관측제", "전사 의식", "치유 의식", "탄생 축복"
        ]
        return random.choice(rituals)
    
    def _generate_value(self, dna: Dict) -> str:
        """가치관 생성"""
        values = [
            "용기", "지혜", "화합", "정의", "자유", 
            "충성", "창의", "인내", "겸손", "호기심"
        ]
        return random.choice(values)
    
    def _add_cultural_element(self, entity: Dict, category: str, element: str):
        """문화 요소 추가 (중복 방지)"""
        if "culture" not in entity:
            entity["culture"] = {"values": [], "taboos": [], "myths": [], "rituals": []}
        
        if element not in entity["culture"].get(category, []):
            if len(entity["culture"].get(category, [])) < 20:  # 최대 20개 제한
                entity["culture"][category].append(element)
    
    def _check_stage_advancement(self, entity: Dict):
        """문명 단계 발전 체크"""
        current_stage = entity.get("stage", 0)
        
        # 단계별 발전 조건
        requirements = {
            0: {"population": 100, "culture_count": 3},    # 원시 → 부족
            1: {"population": 1000, "culture_count": 8},   # 부족 → 초기문명
            2: {"population": 10000, "culture_count": 15}, # 초기문명 → 고전
            3: {"population": 100000, "technology": 5},    # 고전 → 중세
            4: {"population": 500000, "technology": 15},   # 중세 → 산업
            5: {"population": 1000000, "technology": 30},  # 산업 → 정보
        }
        
        if current_stage in requirements:
            req = requirements[current_stage]
            pop_ok = entity["population"] >= req["population"]
            
            culture_count = sum(len(v) for v in entity.get("culture", {}).values())
            culture_ok = culture_count >= req.get("culture_count", 0)
            
            tech_ok = len(entity.get("technology", [])) >= req.get("technology", 0)
            
            if pop_ok and culture_ok and tech_ok:
                entity["stage"] = current_stage + 1
                self.new_events.append({
                    "epoch": self.current_epoch,
                    "type": "stage_advancement",
                    "entity": entity["id"],
                    "from_stage": current_stage,
                    "to_stage": current_stage + 1
                })
    
    def _apply_dna_drift(self, entity: Dict):
        """DNA 서서히 변화"""
        if random.random() < 0.01:  # 1% 확률로 미세 변화
            if "dna" in entity and "innate" in entity["dna"]:
                trait = random.choice(list(entity["dna"]["innate"].keys()))
                drift = random.uniform(-0.1, 0.1)
                current = entity["dna"]["innate"][trait]
                new_value = max(0, min(10, current + drift))
                entity["dna"]["innate"][trait] = round(new_value, 1)
    
    def _check_contacts(self):
        """집단 간 접촉 체크"""
        entities = self.world.get("entities", {}).get("planet_2", [])
        
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                if entity1["id"] in entity2.get("relations", {}):
                    continue  # 이미 접촉함
                
                # 탐험 성향에 따른 접촉 확률
                explore1 = entity1.get("dna", {}).get("expressed", {}).get("exploration", 5)
                explore2 = entity2.get("dna", {}).get("expressed", {}).get("exploration", 5)
                
                contact_chance = (explore1 + explore2) / 2000  # 기본 낮은 확률
                
                if random.random() < contact_chance:
                    self._make_contact(entity1, entity2)
    
    def _make_contact(self, entity1: Dict, entity2: Dict):
        """첫 접촉 처리"""
        # DNA 호환성 계산
        dna1 = entity1.get("dna", {}).get("innate", {})
        dna2 = entity2.get("dna", {}).get("innate", {})
        
        compatibility = 5  # 기본값
        
        # 공격성 차이
        agg_diff = abs(dna1.get("aggression", 5) - dna2.get("aggression", 5))
        compatibility -= agg_diff * 0.3
        
        # 사회성 합
        soc_sum = dna1.get("sociality", 5) + dna2.get("sociality", 5)
        compatibility += (soc_sum - 10) * 0.2
        
        # 관계 결정
        if compatibility > 6:
            relation = "friendly"
        elif compatibility > 3:
            relation = "neutral"
        else:
            relation = "hostile"
        
        # 관계 기록
        if "relations" not in entity1:
            entity1["relations"] = {}
        if "relations" not in entity2:
            entity2["relations"] = {}
            
        entity1["relations"][entity2["id"]] = {
            "status": relation,
            "first_contact": self.current_epoch,
            "compatibility": round(compatibility, 1)
        }
        entity2["relations"][entity1["id"]] = {
            "status": relation,
            "first_contact": self.current_epoch,
            "compatibility": round(compatibility, 1)
        }
        
        # 이벤트 기록
        self.new_events.append({
            "epoch": self.current_epoch,
            "type": "first_contact",
            "parties": [entity1["id"], entity2["id"]],
            "initial_relation": relation
        })
    
    def _check_discoveries(self):
        """자원 발견 체크"""
        # planet_2의 특수 자원들
        special_resources = self.world.get("stellar_system", {}).get("bodies", [])[1].get("special_resources", [])
        
        for resource in special_resources:
            if resource.get("discovered"):
                continue
                
            # 해당 위치의 엔티티가 발견할 수 있는지
            for entity in self.world.get("entities", {}).get("planet_2", []):
                location = entity.get("location", {})
                
                # 위치 매칭 (간단한 로직)
                if "south" in resource.get("location", "") and location.get("continent") == "south":
                    # 호기심 + 탐험성향에 따른 발견 확률
                    dna = entity.get("dna", {}).get("innate", {})
                    discovery_chance = dna.get("curiosity", 5) / 10000
                    
                    if random.random() < discovery_chance:
                        resource["discovered"] = True
                        resource["discovered_by"] = entity["id"]
                        resource["discovered_epoch"] = self.current_epoch
                        
                        self.new_events.append({
                            "epoch": self.current_epoch,
                            "type": "resource_discovery",
                            "resource": resource["type"],
                            "discoverer": entity["id"]
                        })
    
    def _check_new_life(self):
        """새 생명 발생 체크"""
        for body in self.world.get("stellar_system", {}).get("bodies", []):
            life = body.get("life", {})
            
            if life.get("status") == "possible" and life.get("started") is None:
                prob = life.get("emergence_probability", 0)
                
                if random.random() < prob:
                    # 새 생명 탄생!
                    life["status"] = "active"
                    life["started"] = self.current_epoch
                    
                    # 새 엔티티 생성
                    new_entity = self._generate_new_life(body["id"])
                    
                    if body["id"] not in self.world["entities"]:
                        self.world["entities"][body["id"]] = []
                    self.world["entities"][body["id"]].append(new_entity)
                    
                    self.new_events.append({
                        "epoch": self.current_epoch,
                        "type": "life_emergence",
                        "location": body["id"],
                        "entity": new_entity["id"]
                    })
    
    def _generate_new_life(self, planet_id: str) -> Dict:
        """새 생명체 생성"""
        return {
            "id": f"life_{planet_id}_{self.current_epoch}",
            "name": None,
            "nickname": f"{planet_id}의 첫 생명",
            "location": {
                "planet": planet_id,
                "terrain": "unknown"
            },
            "population": 20,
            "stage": 0,
            "dna": {
                "innate": {
                    "curiosity": random.randint(1, 10),
                    "aggression": random.randint(1, 10),
                    "sociality": random.randint(1, 10),
                    "adaptability": random.randint(1, 10),
                    "spirituality": random.randint(1, 10),
                    "ambition": random.randint(1, 10),
                    "cosmic_sensitivity": random.randint(1, 10),
                    "loneliness_awareness": random.randint(1, 10)
                },
                "environmental": {},
                "expressed": {}
            },
            "traits": [],
            "culture": {"values": [], "taboos": [], "myths": [], "rituals": []},
            "relations": {},
            "history": [],
            "discovered_resources": [],
            "technology": []
        }
    
    def _record_event(self, accident: Dict, response: str, entity: Dict):
        """이벤트 기록"""
        event = {
            "epoch": self.current_epoch,
            "accident": accident,
            "response": response,
            "affected_entity": entity["id"],
            "population_after": entity["population"]
        }
        
        if "history" not in entity:
            entity["history"] = []
        entity["history"].append(event)
        
        # 최근 100개만 유지
        if len(entity["history"]) > 100:
            entity["history"] = entity["history"][-100:]
    
    def _select_random_entity(self) -> Dict:
        """랜덤 엔티티 선택"""
        all_entities = []
        for planet_entities in self.world.get("entities", {}).values():
            all_entities.extend(planet_entities)
        
        return random.choice(all_entities) if all_entities else None
    
    def _get_entity(self, entity_id: str) -> Dict:
        """ID로 엔티티 찾기"""
        for planet_entities in self.world.get("entities", {}).values():
            for entity in planet_entities:
                if entity["id"] == entity_id:
                    return entity
        return None
    
    def _update_world_state(self):
        """월드 상태 업데이트"""
        self.world["universe"]["current_epoch"] = self.current_epoch
        self.world["universe"]["last_accessed"] = datetime.now().strftime("%Y-%m-%d")
        
        # 히스토리에 이벤트 추가
        if "history" not in self.world:
            self.world["history"] = {"major_events": [], "accidents": [], "discoveries": [], "contacts": [], "extinctions": []}
        
        for event in self.new_events:
            if event["type"] == "first_contact":
                self.world["history"]["contacts"].append(event)
            elif event["type"] == "stage_advancement":
                self.world["history"]["major_events"].append(event)
            elif event["type"] == "resource_discovery":
                self.world["history"]["discoveries"].append(event)
            elif event["type"] == "life_emergence":
                self.world["history"]["major_events"].append(event)
        
        for accident in self.new_accidents:
            self.world["history"]["accidents"].append(accident)
        
        # 최근 500개만 유지
        for key in self.world["history"]:
            if len(self.world["history"][key]) > 500:
                self.world["history"][key] = self.world["history"][key][-500:]
        
        # 메타 정보 업데이트
        self.world["meta"]["total_epochs_evolved"] += EPOCHS_PER_RUN
        self.world["meta"]["last_save"] = datetime.now().isoformat() + "Z"


def main():
    """메인 실행"""
    import requests
    
    # 환경 변수에서 설정 읽기
    gist_id = os.environ.get("GIST_ID")
    github_token = os.environ.get("GITHUB_TOKEN")
    
    if not gist_id or not github_token:
        print("Error: GIST_ID and GITHUB_TOKEN environment variables required")
        return
    
    # Gist에서 현재 상태 읽기
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching gist: {response.status_code}")
        return
    
    gist_data = response.json()
    
    # JSON 파일 찾기
    json_file = None
    for filename, file_info in gist_data.get("files", {}).items():
        if filename.endswith(".json"):
            json_file = (filename, file_info["content"])
            break
    
    if not json_file:
        print("Error: No JSON file found in gist")
        return
    
    filename, content = json_file
    world_state = json.loads(content)
    
    # 진화 실행
    print(f"Starting evolution from epoch {world_state['universe']['current_epoch']}")
    
    engine = EvolutionEngine(world_state)
    updated_state = engine.evolve(EPOCHS_PER_RUN)
    
    print(f"Evolution complete. Now at epoch {updated_state['universe']['current_epoch']}")
    print(f"New events: {len(engine.new_events)}")
    print(f"New accidents: {len(engine.new_accidents)}")
    
    # Gist 업데이트
    update_data = {
        "files": {
            filename: {
                "content": json.dumps(updated_state, ensure_ascii=False, indent=2)
            }
        }
    }
    
    response = requests.patch(
        f"https://api.github.com/gists/{gist_id}",
        headers=headers,
        json=update_data
    )
    
    if response.status_code == 200:
        print("Gist updated successfully")
    else:
        print(f"Error updating gist: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
