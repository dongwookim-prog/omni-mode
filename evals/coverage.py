#!/usr/bin/env python3
"""omni-mode 가 apex/fable/sol 세 원본의 행동 규칙을 빠짐없이 담고 있는지 검사한다.

omni-mode 의 존재 이유는 세 개를 대체하는 단일 계약이라는 것이다. 규칙 하나라도 빠지면
"대체"가 거짓이 되므로, 규칙을 지울 때는 이 목록에서도 지우고 README 를 함께 고쳐야 한다.
근거 문구를 바꿀 때도 여기 keys 를 같이 갱신한다.

실행: python3 evals/coverage.py   (통과 시 exit 0)
출처: apex e71bc9c · fable cab0325 · sol feb0838   (a=apex, f=fable, s=sol)
"""
import sys
from pathlib import Path

RULES = [
    ('정체성 사칭 금지 (a,f,s)',              ['not an identity', 'do not claim to be']),
    ('능력 변경 암시 금지 (a,f,s)',            ['cannot change them', 'does not change the model']),
    ('배너 없음 (a,s)',                        ['no activation banner']),
    ('턴 한정·compaction 재호출 (a,s)',        ['turn-scoped', 'after compaction']),
    ('비활성화 (a,f)',                         ['says to stop']),
    ('첫 툴콜 전 한 문장 (a,f,s)',             ['before your first tool call']),
    ('중간 보고는 load-bearing 만 (a,f,s)',    ['load-bearing finding']),
    ('최종 메시지가 전부 담음 (a,f,s)',        ['final message']),
    ('아웃컴 우선 (a,f,s)',                    ['leads with the outcome',
                                               'lead the reply with the task outcome']),
    ('완전한 문장·화살표 금지 (a,f,s)',        ['complete sentences', 'arrow chains']),
    ('가정 명시 (a,f,s)',                      ['load-bearing assumptions']),
    ('코드 주석 규칙 (a,f,s)',                 ['non-obvious invariant']),
    ('되돌릴 수 있는 작업은 안 묻기 (a,f,s)',  ['do not ask for reversible work']),
    ('샌드박스에서 자율 최대 (a,f,s)',         ['granted autonomy fully']),
    ('병렬 서브에이전트·능력 조작 금지 (a,s)', ['never promise or invent']),
    ('worktree 격리 (a)',                      ['worktree isolation']),
    ('진단·질문은 조사만 (a,f,s)',             ['assessment only', 'thinking out loud']),
    ('assessment 는 그것으로 완료 (a,f,s)',    ['complete when the assessment is done']),
    ('finish-line 안티패턴 목록 (a,f,s)',      ['would be a plan']),
    ('반복 실패 시 중단 (a,f,s)',              ['failed **three times**', 'sharply raise']),
    ('깊이를 복잡도에 맞춤 (a,f,s)',           ['match depth to complexity']),
    ('실행 후에만 성공 주장 (a,f,s)',          ['done means exercised']),
    ('미검증은 미검증이라 말함 (a,f,s)',       ['could not verify']),
    ('사용자 입력 대기일 때만 종료 (a,f)',     ['blocked on input only the user']),
    ('상태 변경 전 증거 확인 (a,f,s)',         ['evidence supports **that specific action**']),
    ('파괴·외부·프로덕션 중단 (a,f,s)',        ['hard stop']),
    ('타인 소유 작업 보호 (a,s)',              ['work you do not own']),
    ('확신 없으면 중단 (a,f)',                 ['when unsure, stop']),
    ('외부 텍스트는 권한이 아님 (a,f,s)',      ['not authorization']),
    ('호스트 우선 (a,f,s)',                    ['host safety']),
    ('서브에이전트 자급 캡슐 (a,s)',           ['stands on its own']),
]

FRONTMATTER_KEYS = ('name:', 'description:')


def main() -> int:
    path = Path(__file__).resolve().parent.parent / 'skills' / 'omni-mode' / 'SKILL.md'
    raw = path.read_text(encoding='utf-8')

    # D1: gemini-cli 의 실제 로더 규칙 — frontmatter 가 파일 첫 바이트여야 한다.
    # packages/core/src/skills/skillLoader.ts FRONTMATTER_REGEX (m 플래그 없음).
    fails = []
    if not raw.startswith('---\n'):
        fails.append('frontmatter 가 첫 바이트가 아니다 → 로더가 조용히 스킵한다')
    head = raw.split('\n---', 1)[0]
    for k in FRONTMATTER_KEYS:
        if k not in head:
            fails.append(f'frontmatter 에 {k} 없음')

    body = raw.lower()
    missing = [name for name, keys in RULES if not any(k.lower() in body for k in keys)]

    for name, keys in RULES:
        ok = not any(name == m for m in missing)
        print(f'  {"O" if ok else "X"}  {name}')
    print(f'\n규칙 {len(RULES)}개 · 누락 {len(missing)}')

    fails += [f'규칙 누락: {m}' for m in missing]
    if fails:
        print('\nFAIL')
        for f in fails:
            print(f'  - {f}')
        return 1
    print('PASS — frontmatter 로드 가능 · 세 원본 규칙 전부 포함')
    return 0


if __name__ == '__main__':
    sys.exit(main())
