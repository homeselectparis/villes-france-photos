// Helper sans dépendance pour accéder aux photos de villes depuis n'importe
// quel projet. Copiez ce fichier, ou construisez les URLs directement :
// https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main/photos/{slug}.jpg

export const RAW_BASE =
  "https://raw.githubusercontent.com/homeselectparis/villes-france-photos/main";

export const CDN_BASE =
  "https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main";

/**
 * URL publique d'une photo de ville.
 * @param {string} slug - slug de la ville ("paris", "aix-en-provence"...)
 * @param {{ cdn?: boolean }} [options] - cdn: true (défaut) via jsDelivr, false via raw GitHub
 * @returns {string} URL de la photo
 */
export function photoUrl(slug, { cdn = true } = {}) {
  return `${cdn ? CDN_BASE : RAW_BASE}/photos/${slug}.jpg`;
}

/**
 * URL du manifeste complet (liste des villes, licences, crédits).
 * @param {{ cdn?: boolean }} [options]
 * @returns {string} URL du manifest.json
 */
export function manifestUrl({ cdn = false } = {}) {
  return `${cdn ? CDN_BASE : RAW_BASE}/manifest.json`;
}
