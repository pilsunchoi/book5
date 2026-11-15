/* 휴대폰에서 사이드바 토글이 안 열리는 문제 (2026-11-15).
   pydata-sphinx-theme(0.17)과 sphinx-book-theme(1.3)는 사이드바를 여는 동작을 페이지의 "첫 번째" .primary-toggle,
   .secondary-toggle에만 붙인다. 그 첫 번째 버튼은 위쪽 머리줄(.bd-header)에 있어 화면에 보이지 않고, 실제로 보이는
   본문 위 버튼("Toggle primary sidebar", "Toggle secondary sidebar")에는 아무 동작이 없다.
   → 보이는 버튼을 누르면 첫 번째 버튼을 대신 누른다. 데스크톱의 접기 동작(sphinx-book-theme)도 첫 번째 버튼에 붙어 있어 함께 산다. */
document.addEventListener("DOMContentLoaded", () => {
  for (const kind of ["primary", "secondary"]) {
    const buttons = [...document.querySelectorAll(`.${kind}-toggle`)];
    const first = buttons[0];
    buttons.slice(1).forEach((b) =>
      b.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        first.click();
      })
    );
  }
});
