/**
 * 서류 발급 기관(경찰서, 병원)에서 사용할 스크립트
 * 다국어 지원
 */

export const INSTITUTION_SCRIPTS = {
  // 경찰서에서 사용할 스크립트
  police: {
    en: {
      title: 'What to Say at the Police Station',
      greeting: 'Hello, I need to report a theft/loss.',
      main: 'I would like to file a police report for stolen/lost items during my trip. Could you please issue a Police Report for my travel insurance claim?',
      items: 'The stolen/lost items are [describe items here].',
      date: 'The incident occurred on [date] at approximately [time].',
      location: 'It happened at/near [location].',
      closing: 'I need an official Police Report document for my insurance company. Thank you for your assistance.',
      language: 'en-US'
    },
    ko: {
      title: '경찰서에서 할 말',
      greeting: '안녕하세요, 도난/분실 신고를 하러 왔습니다.',
      main: '여행 중 물품을 도난/분실당했습니다. 여행자 보험 청구를 위해 경찰 신고 확인서를 발급받고 싶습니다.',
      items: '도난/분실된 물품은 [물품 설명]입니다.',
      date: '사고는 [날짜] [시간]경에 발생했습니다.',
      location: '[장소]에서 발생했습니다.',
      closing: '보험사에 제출할 공식 경찰 신고 확인서가 필요합니다. 도움 주셔서 감사합니다.',
      language: 'ko-KR'
    },
    ja: {
      title: '警察署での会話',
      greeting: 'こんにちは、盗難・紛失の届出をしたいのですが。',
      main: '旅行中に荷物が盗まれた・紛失しました。旅行保険の請求のため、警察の証明書を発行していただきたいです。',
      items: '盗まれた・紛失した物品は[品物の説明]です。',
      date: '事件は[日付]の[時刻]頃に発生しました。',
      location: '[場所]で発生しました。',
      closing: '保険会社に提出する公式な警察証明書が必要です。ご協力ありがとうございます。',
      language: 'ja-JP'
    },
    es: {
      title: 'Qué decir en la comisaría',
      greeting: 'Hola, necesito reportar un robo/pérdida.',
      main: 'Me gustaría presentar un informe policial por artículos robados/perdidos durante mi viaje. ¿Podría emitir un informe policial para mi reclamo de seguro de viaje?',
      items: 'Los artículos robados/perdidos son [describir artículos aquí].',
      date: 'El incidente ocurrió el [fecha] aproximadamente a las [hora].',
      location: 'Sucedió en/cerca de [ubicación].',
      closing: 'Necesito un documento oficial de informe policial para mi compañía de seguros. Gracias por su ayuda.',
      language: 'es-ES'
    },
    fr: {
      title: 'Que dire au poste de police',
      greeting: 'Bonjour, je dois signaler un vol/une perte.',
      main: 'Je voudrais déposer une plainte pour des objets volés/perdus pendant mon voyage. Pourriez-vous émettre un rapport de police pour ma réclamation d\'assurance voyage?',
      items: 'Les articles volés/perdus sont [décrire les articles ici].',
      date: 'L\'incident s\'est produit le [date] vers [heure].',
      location: 'Cela s\'est passé à/près de [lieu].',
      closing: 'J\'ai besoin d\'un document officiel de rapport de police pour ma compagnie d\'assurance. Merci pour votre aide.',
      language: 'fr-FR'
    }
  },

  // 병원에서 사용할 스크립트
  hospital: {
    en: {
      title: 'What to Say at the Hospital',
      greeting: 'Hello, I need medical assistance.',
      main: 'I am a traveler and I need medical treatment. I have travel insurance and will need documentation for my insurance claim.',
      symptoms: 'My symptoms are [describe symptoms].',
      documents: 'For my insurance claim, I will need: a medical certificate (diagnosis), itemized medical bills, and original receipts.',
      insurance: 'I have travel insurance that covers overseas medical expenses. Can you please provide all documents in English if possible?',
      payment: 'I will pay for the treatment now and submit a claim to my insurance company later.',
      closing: 'Please make sure all receipts and documents are original copies. Thank you.',
      language: 'en-US'
    },
    ko: {
      title: '병원에서 할 말',
      greeting: '안녕하세요, 진료가 필요합니다.',
      main: '저는 여행자이며 치료가 필요합니다. 여행자 보험이 있어서 보험 청구용 서류가 필요합니다.',
      symptoms: '증상은 [증상 설명]입니다.',
      documents: '보험 청구를 위해 다음 서류가 필요합니다: 진단서, 진료비 세부 내역서, 영수증 원본.',
      insurance: '해외 의료비를 보상하는 여행자 보험에 가입되어 있습니다. 가능하면 모든 서류를 영문으로 발급해주시겠습니까?',
      payment: '치료비는 지금 지불하고 나중에 보험사에 청구하겠습니다.',
      closing: '모든 영수증과 서류는 원본으로 발급해주세요. 감사합니다.',
      language: 'ko-KR'
    },
    ja: {
      title: '病院での会話',
      greeting: 'こんにちは、診療が必要です。',
      main: '私は旅行者で治療が必要です。旅行保険に加入しており、保険請求用の書類が必要です。',
      symptoms: '症状は[症状の説明]です。',
      documents: '保険請求のため、以下の書類が必要です：診断書、診療費の明細書、領収書の原本。',
      insurance: '海外医療費を補償する旅行保険に加入しています。可能であれば、すべての書類を英語で発行していただけますか？',
      payment: '治療費は今お支払いして、後で保険会社に請求します。',
      closing: 'すべての領収書と書類は原本で発行してください。ありがとうございます。',
      language: 'ja-JP'
    },
    es: {
      title: 'Qué decir en el hospital',
      greeting: 'Hola, necesito asistencia médica.',
      main: 'Soy viajero y necesito tratamiento médico. Tengo seguro de viaje y necesitaré documentación para mi reclamo de seguro.',
      symptoms: 'Mis síntomas son [describir síntomas].',
      documents: 'Para mi reclamo de seguro, necesitaré: un certificado médico (diagnóstico), facturas médicas detalladas y recibos originales.',
      insurance: 'Tengo un seguro de viaje que cubre gastos médicos en el extranjero. ¿Pueden proporcionar todos los documentos en inglés si es posible?',
      payment: 'Pagaré el tratamiento ahora y presentaré un reclamo a mi compañía de seguros más tarde.',
      closing: 'Por favor, asegúrese de que todos los recibos y documentos sean copias originales. Gracias.',
      language: 'es-ES'
    },
    fr: {
      title: 'Que dire à l\'hôpital',
      greeting: 'Bonjour, j\'ai besoin d\'une assistance médicale.',
      main: 'Je suis un voyageur et j\'ai besoin d\'un traitement médical. J\'ai une assurance voyage et j\'aurai besoin de documents pour ma réclamation d\'assurance.',
      symptoms: 'Mes symptômes sont [décrire les symptômes].',
      documents: 'Pour ma réclamation d\'assurance, j\'aurai besoin: d\'un certificat médical (diagnostic), de factures médicales détaillées et de reçus originaux.',
      insurance: 'J\'ai une assurance voyage qui couvre les frais médicaux à l\'étranger. Pouvez-vous fournir tous les documents en anglais si possible?',
      payment: 'Je paierai le traitement maintenant et soumettrai une réclamation à ma compagnie d\'assurance plus tard.',
      closing: 'Veuillez vous assurer que tous les reçus et documents sont des copies originales. Merci.',
      language: 'fr-FR'
    }
  }
}

/**
 * 지원하는 언어 목록
 */
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸', voice: 'en-US' },
  { code: 'ko', name: '한국어', flag: '🇰🇷', voice: 'ko-KR' },
  { code: 'ja', name: '日本語', flag: '🇯🇵', voice: 'ja-JP' },
  { code: 'es', name: 'Español', flag: '🇪🇸', voice: 'es-ES' },
  { code: 'fr', name: 'Français', flag: '🇫🇷', voice: 'fr-FR' }
]

/**
 * 스크립트 타입별 아이콘
 */
export const SCRIPT_ICONS = {
  police: '🚔',
  hospital: '🏥'
}
